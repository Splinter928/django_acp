import paramiko
import json


class JobList:
    """
    Jobs list creation
    """

    def __init__(self, acp):
        self.settings = acp.settings
        self.joblist = ''
        self.formated_joblist = dict()

    def parse_joblist(self):
        """
        Parse jobs list in string format from SLURM
        """
        with paramiko.SSHClient() as client:
            # add server key to list of known hosts and connect to it
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(hostname=self.settings.HOST, username=self.settings.USER,
                           password=self.settings.PASSWORD, port=self.settings.PORT)

            # parse jobs information
            stdin, stdout, stderr = client.exec_command(
                'squeue --format="%.18i %.10P %.45j %.8u %.5t %.10M %.6D %.5C %.20k %.5N"')
            self.joblist = stdout.read().decode('UTF-8')

    def formate_joblist(self):
        """
        Formatting job list to json compatible format
        """
        headers = [
            'jobid',
            'partition',
            'job_name',
            'user',
            'job_condition',
            'calc_time',
            'num_nodes',
            'num_cpus',
            'project',
            'nodes',
        ]  # headers of job table
        for job in self.joblist.split('\n')[1:]:
            jlist = job.split()  # list of current job attributes
            if jlist:
                if len(jlist) != len(headers):
                    jnodes = ''
                elif jlist[-1].strip('n').isdigit():
                    jnodes = [jlist[-1].strip('n')]
                else:
                    node_start = int(jlist[-1].strip('n[]').split('-')[0])
                    node_fin = int(jlist[-1].strip('n[]').split('-')[1])
                    jnodes = [str(num) for num in range(node_start, node_fin + 1)]
                if jnodes:
                    self.formated_joblist[jlist[0]] = {headers[i]: jlist[i] for i in range(len(headers))}
                else:
                    self.formated_joblist[jlist[0]] = {headers[i]: jlist[i] for i in range(len(headers) - 1)}

    def json_jobfilecreation(self):
        """
        Create JSON file with all jobs information
        """
        with open("acp/parse_data/job_list.json", "w") as write_file:
            json.dump(self.formated_joblist, write_file, indent=4)

    def prepare_json_joblist(self):
        """
        All actions for creating JSON job list
        """
        self.parse_joblist()
        self.formate_joblist()
        self.json_jobfilecreation()
