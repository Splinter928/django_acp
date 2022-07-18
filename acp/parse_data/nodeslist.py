import paramiko
import time


class NodeList:
    """
    Nodes list creation
    """

    def __init__(self, acp):
        self.settings = acp.settings
        self.nodelist = ''
        self.formated_nodelist = dict()

    def parse_nodelist(self):
        """
        Parse node list in string format from SLURM
        """
        with paramiko.SSHClient() as client:
            # add server key to list of known hosts and connect to it
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.settings.HOST, username=self.settings.USER,
                           password=self.settings.PASSWORD, port=self.settings.PORT)

            # parse nodes information
            stdin, stdout, stderr = client.exec_command(
                'sinfo --format="%.15N %.20P %.13T %.4c %.15C %.10m %.10d" --Node')
            self.nodelist = stdout.read().decode('UTF-8')


    def formate_nodelist(self):
        """
        Formatting nodes list to json compatible format
        """
        for nodes in self.nodelist.split('\n')[1:]:
            node = nodes.split()  # list of current node attributes
            if node:
                # creation of new node if it doesn't exist
                if node[0] not in self.formated_nodelist:
                    self.formated_nodelist[node[0]] = {
                        'node': node[0],
                        'partition': node[1].strip('*'),
                        'status': node[2],
                        'cpus': node[3],
                        'cpus_status': node[4],
                        'memory': node[5],
                        'tmp': node[6],
                    }
                # if node already exists in nodelist add new partition to it
                else:
                    self.formated_nodelist[node[0]]['partition'] = self.formated_nodelist[node[0]]['partition'] \
                                                                   + ' ' + node[1].strip('*')

