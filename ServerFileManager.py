class ServerFileManager(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.servers = []

    def read_server_data(self):
        with open(self.file_path, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 2:
                    ip_address, hostname = parts
                    self.servers.append({
                        'ip_address': ip_address,
                        'hostname': hostname,
                        'original_ip': None,
                        'changed': False
                    })

        with open(self.file_path, 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) == 4:
                    ip_address, hostname, original_ip, changed = parts
                    self.servers.append({
                        'ip_address': ip_address,
                        'hostname': hostname,
                        'original_ip': original_ip,
                        'changed': changed
                    })

    def update_server_ip(self, hostname, new_ip, ip):
        for server in self.servers:
            if server['hostname'] == hostname:
                server['ip_address'] = new_ip
                server['original_ip'] = ip
                server['changed'] = True

    def save_changes(self):
        with open(self.file_path, 'w') as file:
            for server in self.servers:
                line = f"{server['host']} {server['changed_ip'] if server['changed'] else server['original_ip']} {'true' if server['changed'] else 'false'}\n"
                file.write(line)




