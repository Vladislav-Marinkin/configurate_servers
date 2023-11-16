#from typing import Self
import paramiko

from UserDialog import UserDialog

class SSHClient(object):
    def __init__(self, ip, user_dialog, hostname = None, port=22):
        self.ip = ip
        self.hostname = hostname
        self.port = port
        self.client = paramiko.SSHClient()
        self.user_dialog = user_dialog

    def connect_to_server(self, ip=None):
        # Если IP не предоставлен явно, используем IP из экземпляра класса
        if ip is None:
            ip = self.ip

        # Загружаем системные ключи и устанавливаем политику добавления отсутствующих ключей
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            # Если включено использование отдельных логина и пароля
            if self.user_dialog.use_login_password_separately:
                self.user_dialog.prompt_login_credentials(ip)

            # Подключение к серверу
            if self.user_dialog.key_filename is None:
                # Подключение с использованием логина и пароля
                self.client.connect(ip, self.port, self.user_dialog.username, self.user_dialog.password)
            else:
                # Подключение с использованием логина и ключа
                self.client.connect(ip, self.port, username=self.user_dialog.username, key_filename=self.user_dialog.key_filename)

            # Выводим сообщение об успешном подключении
            print(f"Connected to server {self.ip}")

            # Возвращаем объект клиента для дальнейшего использования
            return self.client
        except paramiko.AuthenticationException:
            # Выводим сообщение об ошибке аутентификации
            print(f"Error connecting to server {self.hostname}")
            print(paramiko.AuthenticationException.with_traceback)
            return None

    def close(self):
        self.client.close()
        print(f"Connection to {self.hostname} closed")

    def execute_command(self, command):
        # Создаем новый канал
        channel = self.client.get_transport().open_session()

        # Запускаем команду
        channel.exec_command(command)
        result = channel.recv(4096).decode("utf-8")

        # Ждем завершения выполнения команды
        channel.recv_exit_status()

        # Возвращаем ответ
        return result

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

    def backup_exists(self, patch):
        command = f"ls {patch}.bak"
        result = self.execute_command(command)

        if result == "":
            return False
        else:
            return True

    def create_backup(self, patch):
        command = f"cp {patch} {patch}.bak"
        self.execute_command_with_sudo(command)

    def change_netplan_config(self, file_manager):
        # Создаем бэкап файла
        patch = "/etc/netplan/00-installer-config.yaml"
        if not self.backup_exists(patch):
            self.create_backup(patch)

        if self.checking_changes_already_made(file_manager.servers):
            return

        new_ip = self.user_dialog.enter_new_ip(self.hostname)

        command = f"""sh -c 'echo "# This is the network config written by 'subiquity'\nnetwork:\n  ethernets:\n    eth0:\n      addresses:\n        - {new_ip}/24\n      routes:\n        - to: 0.0.0.0/0\n          via: 192.168.0.1\n      nameservers:\n          addresses: [8.8.8.8, 8.8.4.4]\n  version: 2" > /etc/netplan/00-installer-config.yaml'"""
        
        self.execute_command_with_sudo(command)

        file_manager.update_server_ip(self.hostname, new_ip, self.ip)

    def change_hostname(self):
        # Команда для изменения хостнейма
        command = f"hostnamectl set-hostname {self.hostname}"

        # Выполнение команды
        self.execute_command_with_sudo(command)

        # Перезагрузка для применения изменений (опционально)
        # execute_command_with_sudo(client, "reboot")

    def modify_hosts_file(self, servers):
        # Создаем бэкап файла
        patch = "/etc/hosts"
        if not self.backup_exists(patch):
            self.create_backup(patch)

        # Создаем блок для добавления в /etc/hosts
        dns_block = "#MY DNS BEGIN\n"
        for server in servers:
            if server['hostname'] != self.hostname:
                dns_block += f"{server['ip_address']} {server['hostname']}.local\n"
        dns_block += "#MY DNS END\n"

        # Получаем существующий блок
        command = "sed -n '/#MY DNS BEGIN/,/#MY DNS END/p' /etc/hosts | grep -v '#MY DNS'"
        current_dns_block = self.execute_command(command)
        print(current_dns_block)

        # Удаляем существующий блок
        command = "sed -i '/#MY DNS BEGIN/,/#MY DNS END/d' /etc/hosts"
        self.execute_command_with_sudo(command)

        # Добавляем новый блок DNS в конец файла
        command = f"""sh -c 'echo "{dns_block}" >> /etc/hosts'"""
        self.execute_command_with_sudo(command)

        # Меняем хост в /etc/hosts
        command = f"sed -i '2s/127.0.1.1 test-server-01/127.0.1.1 {self.hostname}/' /etc/hosts"
        self.execute_command_with_sudo(command)

    def get_hostname_server(self):
        command = "hostname"
        self.hostname = self.execute_command(command).strip()