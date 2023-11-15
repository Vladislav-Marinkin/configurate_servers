#from typing import Self
import paramiko

from UserDialog import UserDialog

class SSHClient(object):
    def __init__(self, ip, hostname, user_dialog, port=22):
        self.ip = ip
        self.hostname = hostname
        self.port = port
        self.client = paramiko.SSHClient()
        self.user_dialog = user_dialog

    def connect_to_server(self):
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            if self.user_dialog.use_login_password_separately:
                self.user_dialog.prompt_login_credentials(self.ip)

            if self.user_dialog.key_filename == None:
                self.client.connect(self.ip, self.port, self.user_dialog.username, self.user_dialog.password)
            else:
                self.client.connect(self.ip, self.port, username=self.user_dialog.username, key_filename=self.user_dialog.key_filename)
            
            print(f"Connected to server {self.hostname}")

            return self.client
        except paramiko.AuthenticationException:
            print(f"Error connecting to server {self.hostname}")
            print(paramiko.AuthenticationException.with_traceback)
            return None

    def close(self):
        self.client.close()
        print(f"Connection to {self.hostname} closed")

    def execute_command_with_sudo(self, command):
        # Создаем новый канал
        channel = self.client.get_transport().open_session()
    
        # Запускаем команду с sudo
        command_with_sudo = f"echo '{self.user_dialog.sudo_password}' | sudo -S {command}"
        channel.exec_command(command_with_sudo)

        # Ждем завершения выполнения команды
        channel.recv_exit_status()

    def checking_changes_already_made(self, servers):
        return any(server['changed'] for server in servers if server['hostname'] == self.hostname)

    def change_netplan_config(self, file_manager):
        if self.checking_changes_already_made(file_manager.servers):
            return

        new_ip = self.user_dialog.enter_new_ip(self.hostname)

        command = f"""sh -c 'echo "# This is the network config written by 'subiquity'\nnetwork:\n  ethernets:\n    eth0:\n      addresses:\n        - {new_ip}/24\n      routes:\n        - to: 0.0.0.0/0\n          via: 192.168.0.1\n      nameservers:\n          addresses: [8.8.8.8, 8.8.4.4]\n  version: 2" > /etc/netplan/00-installer-config.yaml'"""
        #command = """sh -c 'echo "# This is the network config written by 'subiquity'\nnetwork:\n  ethernets:\n    eth0:\n      dhcp4: true\n  version: 2" > /etc/netplan/00-installer-config.yaml'"""
        
        self.execute_command_with_sudo(command)

        file_manager.update_server_ip(self.hostname, new_ip, self.ip)

    def change_hostname(self):
        # Команда для изменения хостнейма
        #self.hostname = "test"
        command = f"hostnamectl set-hostname {self.hostname}"

        # Выполнение команды
        self.execute_command_with_sudo(command)

        # Перезагрузка для применения изменений (опционально)
        # execute_command_with_sudo(client, "sudo reboot")

#    def modify_hosts_file(self):
        # Создаем блок для добавления в /etc/hosts
#        dns_block = "#MY DNS BEGIN\n"
#        for server in server_data:
#            if current_server['hostname'] != server['hostname']:
#                dns_block += f"{server['ip_address_to_assign']} {server['hostname']}.local\n"
#        dns_block += "#MY DNS END\n"