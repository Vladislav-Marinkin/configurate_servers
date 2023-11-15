import threading
import time

from ServerFileManager import ServerFileManager
from SSHClient import SSHClient
from UserDialog import UserDialog

if __name__ == "__main__":
    # ������� ��������� ������ ServerFileManager
    file_manager = ServerFileManager("servers_ip_adresses.ini")
    file_manager.read_server_data()

    # ����������� ����� � ������, ���� ��� ���������, ��� ����� ����� ��� ������� ������� ����� ������
    user_dialog = UserDialog()
    user_dialog.prompt_login_credentials()

    # ���������� ���������� ������ SSHClient � ���� servers
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