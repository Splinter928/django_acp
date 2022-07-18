import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_acp.settings'
import django

django.setup()

import time
from acp.parse_data.partitionlist import PartitionList
from acp.parse_data.joblist import JobList
from acp.parse_data.nodeslist import NodeList
from acp.parse_data.connection_settings import Settings
from acp.models import Partition, Job, Node


class DbFill:

    def __init__(self):
        self.settings = Settings()
        self.partlist = PartitionList(self)
        self.joblist = JobList(self)
        self.nodelist = NodeList(self)

    def data_parse(self):
        """
        Parsing and formatting partitions, jobs and summary from SLURM
        """
        self.partlist.parse_partlist()
        self.partlist.formate_partlist()
        self.partlist.formate_summary()
        # self.partlist.json_summarycreation()

        self.joblist.parse_joblist()
        self.joblist.formate_joblist()

        self.nodelist.parse_nodelist()
        self.nodelist.formate_nodelist()

    def partitions_to_db(self):
        """
        Filling in database with actual partitionlist
        """
        bulk_updates, bulk_creates, bulk_deletes = [], [], []
        partitions = Partition.objects.all()
        partitions_names = []

        # update existing partitions and create list of deleted partitions
        for partition in partitions:
            partitions_names.append(partition.name)
            if partition.name in self.partlist.formated_partlist:
                partition.avail = self.partlist.formated_partlist[partition.name]['avail']
                partition.nodes_count = self.partlist.formated_partlist[partition.name]['nodes_count']
                partition.nodes_status = self.partlist.formated_partlist[partition.name]['nodes_status']
                partition.cpus_status = self.partlist.formated_partlist[partition.name]['cpus_status']
                partition.small_nodes_list = self.partlist.formated_partlist[partition.name]['small_nodes_list']
                partition.all_nodes_list = self.partlist.formated_partlist[partition.name]['all_nodes_list']
            else:
                bulk_deletes.append(partition.name)
        Partition.objects.bulk_update(partitions, ['avail', 'nodes_count', 'cpus_status',
                                                   'small_nodes_list', 'all_nodes_list'])

        # create list of new partitions from parsed data
        for parsed_partition in self.partlist.formated_partlist:
            if parsed_partition not in partitions_names:
                bulk_creates.append(Partition(**self.partlist.formated_partlist[parsed_partition]))

        # create\delete partitions in DB, if it is necessary
        if bulk_creates:
            Partition.objects.bulk_create(bulk_creates)
        if bulk_deletes:
            Partition.objects.filter(name__in=bulk_deletes).delete()

    def nodes_to_db(self):
        """
        Updating nodes in database and clearing non-actual nodes
        """
        bulk_updates, bulk_creates, bulk_deletes = [], [], []
        nodes = Node.objects.all()
        nodes_names = []

        # update existing partitions and create list of deleted partitions
        for node in nodes:
            nodes_names.append(node.node)
            if node.node in self.nodelist.formated_nodelist:
                node.partition = self.nodelist.formated_nodelist[node.node]['partition']
                node.status = self.nodelist.formated_nodelist[node.node]['status']
                node.cpus_status = self.nodelist.formated_nodelist[node.node]['cpus_status']
            else:
                bulk_deletes.append(node.node)
        Node.objects.bulk_update(nodes, ['partition', 'status', 'cpus_status'])

        # create list of new nodes from parsed data
        for parsed_node in self.nodelist.formated_nodelist:
            if parsed_node not in nodes_names:
                bulk_creates.append(Node(**self.nodelist.formated_nodelist[parsed_node]))

        # create\delete nodes in DB, if it is necessary
        if bulk_creates:
            Node.objects.bulk_create(bulk_creates)
        if bulk_deletes:
            Node.objects.filter(name__in=bulk_deletes).delete()

    def jobs_to_db(self):
        """
        Clearing old jobs and filling in database with actual jobs
        """
        Job.objects.all().delete()
        Job.objects.bulk_create([Job(**self.joblist.formated_joblist[job]) for job in self.joblist.formated_joblist])

    def filling_db(self):
        self.data_parse()
        self.partitions_to_db()
        self.jobs_to_db()
        self.nodes_to_db()


# debugging part:
if __name__ == '__main__':
    j = DbFill()
    j.filling_db()
