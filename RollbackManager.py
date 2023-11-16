class RollbackManager(object):
    def __init__(self, ssh_client, file_manager):
        self.ssh_client = ssh_client
        self.file_manager = file_manager

#    def rollback_changes(self):
        