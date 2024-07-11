from Menu import Menu
from NetworkScanner import NetworkScanner

import os
import time
import ipaddress

class ServerSettingsMenu(Menu):
    def __init__(self):
        super().__init__("Server Settings Menu", [
            "Enter subnet address",
            "Change server configuration",
            "Change hostname",
            "Change hosts settings",
            "Apply netplan settings",
            "Reboot servers"
        ])
        self.subnet = None
        self.hosts = []

    def enter_subnet(self):
        while True:
            self.subnet = input("Enter subnet address (e.g., 192.168.1.1/24): ").strip()
            try:
                subnet = ipaddress.ip_network(self.subnet, strict=False)
                print(f"Subnet address: {self.subnet}")
                self.find_hosts()
                break
            except ValueError:
                print("Invalid subnet address. Please try again.")

    def find_hosts(self):
        print("Finding hosts...")
        network_scanner = NetworkScanner(self.subnet)
            
        

        while True:
            self.hosts = network_scanner.find_hostes()
            
            if any(host['ssh'] for host in network_scanner.hosts):
                self.print_server_list(network_scanner.hosts)
                if not self.check_yes_no("Scan the network again? (yes/no): "):
                    self.hosts = network_scanner.hosts
                    return

            if self.check_yes_no("Search until servers with open SSH port are found? (yes/no): "):
                network_scanner.clietn_ssh = False
                while network_scanner.clietn_ssh:
                    return
        #print(f"Hosts found: {', '.join(self.hosts)}")

    def change_configuration(self):
        print("Changing server configuration...")
        # Implement the logic to change the server configuration here
        time.sleep(1)

    def change_hostname(self):
        for host in self.hosts:
            hostname = input(f"Enter new hostname for {host}: ").strip()
            print(f"Changing hostname for {host} to {hostname}")
            # Implement the logic to change the hostname here
            time.sleep(1)

    def change_hosts_settings(self):
        print("Changing hosts settings...")
        # Implement the logic to change the hosts settings here
        time.sleep(1)

    def apply_netplan_settings(self):
        print("Applying netplan settings...")
        # Implement the logic to apply netplan settings here
        time.sleep(1)

    def reboot_servers(self):
        print("Rebooting servers...")
        # Implement the logic to reboot the servers here
        time.sleep(3)

    def execute(self, choice):
        if choice == 1:
            self.enter_subnet()
        elif choice == 2:
            self.change_configuration()
        elif choice == 3:
            self.change_hostname()
        elif choice == 4:
            self.change_hosts_settings()
        elif choice == 5:
            self.apply_netplan_settings()
        elif choice == 6:
            self.reboot_servers()

class RollbackSettingsMenu(Menu):
    def __init__(self):
        super().__init__("Rollback Settings Menu", [
            "Rollback netplan settings",
            "Rollback hosts settings",
            "Apply netplan settings",
            "Reboot servers"
        ])

    def rollback_netplan_settings(self):
        print("Rolling back netplan settings...")
        # Implement the logic to rollback netplan settings here
        time.sleep(1)

    def rollback_hosts_settings(self):
        print("Rolling back hosts settings...")
        # Implement the logic to rollback hosts settings here
        time.sleep(1)

    def apply_netplan_settings(self):
        print("Applying netplan settings...")
        # Implement the logic to apply netplan settings here
        time.sleep(1)

    def reboot_servers(self):
        print("Rebooting servers...")
        # Implement the logic to reboot the servers here
        time.sleep(3)

    def execute(self, choice):
        if choice == 1:
            self.rollback_netplan_settings()
        elif choice == 2:
            self.rollback_hosts_settings()
        elif choice == 3:
            self.apply_netplan_settings()
        elif choice == 4:
            self.reboot_servers()

class MainMenu(Menu):
    def __init__(self):
        super().__init__("Main Menu", [
            "Change server settings",
            "Rollback server settings",
            "Exit"
        ])
        self.server_settings_menu = ServerSettingsMenu()
        self.rollback_settings_menu = RollbackSettingsMenu()
        self.server_settings_menu.previous_menu = self
        self.rollback_settings_menu.previous_menu = self

    def execute(self, choice):
        if choice == 1:
            self.navigate_to(self.server_settings_menu)
        elif choice == 2:
            self.navigate_to(self.rollback_settings_menu)
        elif choice == 3:
            exit(0)

    def navigate_to(self, menu):
        menu.display()
        choice = menu.get_choice()
        if choice == 'back':
            self.display()
            self.execute(self.get_choice())
        else:
            menu.execute(choice)
            menu.display()
            self.navigate_to(menu)