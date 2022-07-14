import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_acp.settings'
import django

django.setup()

import time
from .partitionlist import PartitionList
from .joblist import JobList
from .nodeslist import NodeList
from .connection_settings import Settings
from acp.models import Partition, Job


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
        self.partlist.json_summarycreation()
        self.joblist.parse_joblist()
        self.joblist.formate_joblist()
        # self.nodelist.parse_nodelist()
        # self.nodelist.formate_nodelist()

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

        # create list of new partitions in DB from parsed data
        for parsed_partition in self.partlist.formated_partlist:
            if parsed_partition not in partitions_names:
                bulk_creates.append(Partition(**self.partlist.formated_partlist[parsed_partition]))

        # create\delete partitions in DB, if it is necessary
        if bulk_creates:
            Partition.objects.bulk_create(bulk_creates)
        if bulk_deletes:
            Partition.objects.filter(name__in=bulk_deletes).delete()

    def jobs_to_db(self):
        """
        Clearing old jobs and filling in database with actual jobs
        """
        Job.objects.all().delete()
        Job.objects.bulk_create([Job(**self.joblist.formated_joblist[job]) for job in self.joblist.formated_joblist])

    def filling_db(self):
        # time1 = time.time()
        self.data_parse()
        # time2 = time.time()
        self.partitions_to_db()
        self.jobs_to_db()
        # print(time2-time1)


# debugging part:
if __name__ == '__main__':
    j = DbFill()
    j.data_parse()
    print(j.nodelist.formated_nodelist)
