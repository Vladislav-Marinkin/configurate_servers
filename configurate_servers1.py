from SSHClient import SSHClient
from UserDialog import UserDialog
from NetworkScanner import NetworkScanner
from SSHClient import SSHClient

if __name__ == "__main__":
    # ����������� ����� � ������, ���� ��� ���������, ��� ����� ����� ��� ������� ������� ����� ������
    user_dialog = UserDialog()
    user_dialog.prompt_login_credentials()

    # ��������� ���� �� ������� ������
    ip = user_dialog.get_subnet_from_user()
    network_scanner = NetworkScanner(ip)
    network_servers = network_scanner.scan(user_dialog)

    # ���������� ���������� ������ SSHClient � ���� servers
    servers = []
    for server in network_servers:
        if server['ssh']:
            ssh_client = SSHClient(server['ip'], user_dialog)
            ssh_client.connect_to_server()
            ssh_client.get_hostname_server()
            servers.append(ssh_client)

    # �������� ������ �������
    servers = user_dialog.server_selection(servers)

    if user_dialog.apply_changes():
        for server in servers:
            server.change_netplan_config()
            server.change_hostname(user_dialog)
        
        for server in servers:
            server.modify_hosts_file(servers)

#        for server in servers:
#            server.reboot_server()
#            server.netplan_apply(user_dialog)

    if user_dialog.rollback_changes():
        for server in servers:
            server.rollback()

    if user_dialog.reboot_server():
        for server in servers:
            server.reboot_server()

    for server in servers:
        server.close()