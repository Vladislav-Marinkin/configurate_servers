import threading
import time

from ServerFileManager import ServerFileManager
from SSHClient import SSHClient
from UserDialog import UserDialog

if __name__ == "__main__":
    # Создаем экземпляр класса ServerFileManager
    file_manager = ServerFileManager("servers_ip_adresses.ini")
    file_manager.read_server_data()

    # Запрашиваем логин и пароль, ключ или указываем, что форма входа для каждого сервера будет разная
    user_dialog = UserDialog()
    user_dialog.prompt_login_credentials()

    # Записываем экземпляры класса SSHClient в лист servers
    servers = []
    for server in file_manager.servers:
        ssh_client = SSHClient(server['ip_address'], server['hostname'], user_dialog)
        ssh_client.connect_to_server()
        servers.append(ssh_client)

    for server in servers:
        server.change_netplan_config(file_manager)
        server.change_hostname()

    for server in servers:
        server.close()
    print("end")