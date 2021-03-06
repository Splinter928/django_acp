import paramiko
import json


class PartitionList:
    """
    Parsing partition list and summary information
    """

    def __init__(self, acp):
        self.settings = acp.settings
        self.partlist = ''
        self.formated_partlist = dict()
        self.summary = []
        self.formated_summary = dict()

    def parse_partlist(self):
        """
        Parse partition list in string format from SLURM
        """
        with paramiko.SSHClient() as client:
            # add server key to list of known hosts and connect to it
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.settings.HOST, username=self.settings.USER,
                           password=self.settings.PASSWORD, port=self.settings.PORT)

            # parse partition information
            stdin, stdout, stderr = client.exec_command('sinfo --format="%.20R %.5a %.20N %.5D %.10A %.15C"')
            self.partlist = stdout.read().decode('UTF-8')

            # parse summary information
            stdin, stdout, stderr = client.exec_command('sinfo -O cpusstate,nodeaiot')
            self.summary += stdout.read().decode('UTF-8').split()

    def formate_partlist(self):
        """
        Formatting partition list to json compatible format
        """
        for partition in self.partlist.split('\n')[1:]:
            plist = partition.split()  # list of current partition attributes
            pnodes = []  # all nodes list for current partition
            if plist:
                for plist_part in plist[2].split(','):
                    if plist_part.strip('n').isdigit():
                        pnodes += [plist_part.strip('n')]
                    else:
                        node_start = int(plist_part.strip('n[]').split('-')[0])
                        node_fin = int(plist_part.strip('n[]').split('-')[1])
                        pnodes += [str(num) for num in range(node_start, node_fin + 1)]

                self.formated_partlist[plist[0]] = {
                    'name': plist[0],
                    'avail': plist[1],
                    'nodes_count': plist[3],
                    'nodes_status': {
                        'alocated': plist[4].split('/')[0],
                        'idle': plist[4].split('/')[1]
                    },
                    'cpus_status': '/'.join([plist[5].split('/')[0], plist[5].split('/')[1], plist[5].split('/')[3]]),
                    'small_nodes_list': plist[2],
                    'all_nodes_list': ' '.join(pnodes),
                }

    def formate_summary(self):
        """
        Formate summary to json compatible format
        """
        self.formated_summary = {
            self.summary[0]: self.summary[2],
            self.summary[1]: self.summary[3],
        }

    def json_plistcreation(self):
        """
        Create JSON file with all partition information
        """
        with open("acp/parse_data/partition_list.json", "w") as write_file:
            json.dump(self.formated_partlist, write_file, indent=4)

    def json_summarycreation(self):
        """
        Create JSON file with summary information
        """
        with open("acp/parse_data/summary.json", "w") as write_file:
            json.dump(self.formated_summary, write_file, indent=4)

    def prepare_json_partlist(self):
        """
        All actions for parsing partitions and summary lists
        """
        self.parse_partlist()
        self.formate_partlist()
        self.json_plistcreation()
        self.formate_summary()
        # self.json_summarycreation()
