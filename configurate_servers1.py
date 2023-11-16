import threading
import time

from ServerFileManager import ServerFileManager
from SSHClient import SSHClient
from UserDialog import UserDialog
from NetworkScanner import NetworkScanner

if __name__ == "__main__":
    # ������� ��������� ������ ServerFileManager
    file_manager = ServerFileManager("servers_ip_adresses.ini")
    file_manager.read_server_data()

    # ����������� ����� � ������, ���� ��� ���������, ��� ����� ����� ��� ������� ������� ����� ������
    user_dialog = UserDialog()
    user_dialog.prompt_login_credentials()

    # ��������� ���� �� ������� ������
    ip = user_dialog.get_subnet_from_user()
    network_scanner = NetworkScanner(ip)
    network_servers = network_scanner.scan()

    # ���������� ���������� ������ SSHClient � ���� servers
    servers = []
    #for server in file_manager.servers:
    for server in network_servers:
        if server['ssh']:
            ssh_client = SSHClient(server['ip'], user_dialog)
            ssh_client.connect_to_server()
            ssh_client.get_hostname_server()
            servers.append(ssh_client)

    # �������� ������ �������
    user_dialog.server_selection(servers)

#    for server in servers:
#        server.change_netplan_config(file_manager)
#        server.change_hostname()
#        server.modify_hosts_file(file_manager.servers)

    for server in servers:
        server.close()