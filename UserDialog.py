import ipaddress
import os
import select
from sys import platform
from wsgiref import validate

class UserDialog(object):
    def __init__(self):
        self.username = None
        self.password = None
        self.sudo_password = None
        self.key_filename = None
        self.use_login_password_separately = False

    def prompt_login_credentials(self, hostname = None):
        if self.use_login_password_separately != True:
            print(f"Enter login credentials for {hostname}")
        else:
            print(f"Enter login credentials for all servers")

        if self.use_login_password_separately != True:
            while True:
                use_login_password_separately = input("Will the input of username and password be performed for each server separately? (yes/no): ").lower()
                if use_login_password_separately in ('yes', 'no'):
                    if use_login_password_separately == 'yes':
                        self.use_login_password_separately = True
                        return
                    else:
                        self.use_login_password_separately = False
                        break
                else:
                    print("Invalid input. Please enter 'yes' or 'no'.")

        while True:
            use_login_password = input("Do you want to use login/password? (yes/no): ").lower()
            if use_login_password in ('yes', 'no'):
                break
            else:
                print("Invalid input. Please enter 'yes' or 'no'.")

        if use_login_password == 'yes':
            self.username = input("Username: ")
            self.password = input("Password: ")
            while True:
                sudo_password = input("Is the entered password different from the superuser password? (yes/no): ")
                if sudo_password in ('yes', 'no'):
                    if sudo_password == 'yes':
                        self.sudo_password = self.password
                        break
                    else:
                        self.sudo_password = input("Superuser password: ")
                        break
        else:
            self.key_path = input("Path to private key file: ")

    def validate_ip(self, ip_address):
        try:
            ipaddress.IPv4Address(ip_address)
            return True
        except ipaddress.AddressValueError:
            return False

    def enter_new_ip(self, hostname):
        print(f"Enter new ip addres for {hostname}")

        while True:
            ip = input("Enter you new ip: ")

            if self.validate_ip(ip):
                return ip
            else:
                print("The IP address is entered incorrectly, try entering it again.")

    def get_subnet_from_user(self):
        while True:
            ip = input("Enter the network for scanning (e.g., '192.168.0.1'): ")

            if self.validate_ip(ip):
                return ip + "/24"
            else:
                print("The IP address is entered incorrectly, try entering it again.")

    def clear_console(self):
        if platform.startswith('win'):
            os.system('cls')
        elif platform.startswith('linux') or platform.startswith('darwin'):
            os.system('clear')

    def server_selection(self, servers):
        self.clear_console()

        i = 0
        for server in servers:
            i += 1
            print(f"{i}) IP: {server.ip}, Hostname: {server.hostname}")

        select_servers = list(map(int, input("Enter number serwers (e.g., 1,2,3): ").split(',')))
        for server in select_servers:


            print(server)