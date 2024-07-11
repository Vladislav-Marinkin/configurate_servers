from email import message
from SSHClient import SSHClient
from UserDialog import UserDialog
from NetworkScanner import NetworkScanner
from SSHClient import SSHClient
from ARGParse import ARGParse
from MainMenu import MainMenu

if __name__ == "__main__":
    main_menu = MainMenu()
    main_menu.display()
    main_menu.execute(main_menu.get_choice())
    
    # arg_parse = argparse()
    # user_dialog = userdialog()
    # if not arg_parse.parse():
    #     # запрашиваем логин и пароль, ключ или указываем, что форма входа для каждого сервера будет разная
    #     user_dialog.prompt_login_credentials()
    #     ip = user_dialog.get_subnet_from_user()
    # else:
    #     user_dialog.username = arg_parse.login
    #     user_dialog.password = arg_parse.password
    #     user_dialog.sudo_password = arg_parse.sudo_password
    #     ip = arg_parse.subnet
        
    # # сканируем сеть на наличие хостов
    # network_scanner = networkscanner(ip, user_dialog)
    # network_scanner.scan()
    
    # # проверка правильности логина и пароля ssh
    # for server in network_scanner.client_list:
    #     if server['ssh']:
    #         ssh_client = sshclient(server['ip'], user_dialog)

    # Записываем экземпляры класса SSHClient в лист servers
    #servers = []
    #for server in network_servers:
        #if server['ssh']:
            #ssh_client = SSHClient(server['ip'], user_dialog)
            #ssh_client.connect_to_server()
            #ssh_client.get_hostname_server()
            #servers.append(ssh_client)

    # Выбираем нужные сервера
    #servers = user_dialog.server_selection(servers)

    # Производим изменения на серверах
    # if user_dialog.apply_changes():
    #     if user_dialog.change_netplan_config():
    #         for server in servers:
    #             server.change_netplan_config()

    #     if user_dialog.change_hostname():
    #         for server in servers:
    #             server.change_hostname(user_dialog)

    #     if user_dialog.modify_hosts_file():
    #         for server in servers:
    #             server.modify_hosts_file(servers)

    # Откат серверов
    # if user_dialog.rollback_changes():
    #     for server in servers:
    #         server.rollback()

    # Перезагрузка серверов
    # if user_dialog.reboot_server():
    #     for server in servers:
    #         server.reboot_server()

    # Закрываем все соединения
    # for server in servers:
    #     server.close()