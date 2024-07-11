import configparser
from http import client
import socket
import time
from scapy.all import ARP, Ether, srp

class NetworkScanner:
    def __init__(self, subnet):
        self.clietn_ssh = False
        self.subnet = subnet
        self.hosts = []
        self.find_time = None
        self.load_settings()
        
    def load_settings(self):
        config = configparser.ConfigParser()
        config.read('settings.ini')
        try:
            self.find_time = config.getint('Settings', 'find_time')
        except (configparser.NoSectionError, configparser.NoOptionError, ValueError) as e:
            print(f"Error reading find time from settings.ini: {e}")
            self.find_time = 15
        
    def find_hostes(self):
        self.perform_scan()
        return self.hosts

    def perform_scan(self):
        #start_time = time.time()
        while not self.client_ssh:#time.time() - start_time < self.find_time:
            if self.clietn_ssh:
                start_time =+ 15

            answered_list = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=self.subnet), timeout=1, verbose=False)[0]

            for answer in answered_list:
                ip, mac = answer[1].psrc, answer[1].hwsrc
                ssh_open = self.check_ssh(ip)
                
                if not any(client['ip'] == ip for client in self.hosts):
                    self.hosts.append({
                        "ip": ip, 
                        "mac": mac, 
                        "ssh": ssh_open
                        #"username": self.user_dialog.username, 
                        #"password": self.user_dialog.password, 
                        #"sudo_password": self.user_dialog.sudo_password
                    })
                    #self.user_dialog.print_server(ip, mac, ssh_open)
                    print(f"ip {ip}, mac {mac}")
                    if ssh_open:
                        self.clietn_ssh = True
                    

    def check_ssh(self, ip, port=22, timeout=3):
        try:
            with socket.create_connection((ip, port), timeout=timeout):
                return True
        except (socket.timeout, ConnectionRefusedError):
            return False