import threading
import time

from ServerFileManager import ServerFileManager
from SSHClient import SSHClient
from UserDialog import UserDialog
from NetworkScanner import NetworkScanner

if __name__ == "__main__":
    # Создаем экземпляр класса ServerFileManager
    file_manager = ServerFileManager("servers_ip_adresses.ini")
    file_manager.read_server_data()

    # Запрашиваем логин и пароль, ключ или указываем, что форма входа для каждого сервера будет разная
    user_dialog = UserDialog()
    user_dialog.prompt_login_credentials()

    # Сканируем сеть на наличие хостов
    ip = user_dialog.get_subnet_from_user()
    network_scanner = NetworkScanner(ip)
    network_servers = network_scanner.scan()

    # Записываем экземпляры класса SSHClient в лист servers
    servers = []
    #for server in file_manager.servers:
    for server in network_servers:
        if server['ssh']:
            ssh_client = SSHClient(server['ip'], user_dialog)
            ssh_client.connect_to_server()
            ssh_client.get_hostname_server()
            servers.append(ssh_client)

    # Выбираем нужные сервера
    user_dialog.server_selection(servers)

#    for server in servers:
#        server.change_netplan_config(file_manager)
#        server.change_hostname()
#        server.modify_hosts_file(file_manager.servers)

    for server in servers:
        server.close()