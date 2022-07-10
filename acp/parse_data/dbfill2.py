import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_acp.settings'
import django

django.setup()

import time
from joblist import JobList
from connection_settings import Settings
from partitionlist import PartitionList
from acp.models import Partition, Job


class DbFill:

    def __init__(self):
        self.settings = Settings()
        self.partlist = PartitionList(self)
        self.joblist = JobList(self)
        self.part_list = {}
        self.jobs_list = {}

    def data_parse(self):
        """
        Parse and formatting partitions and jobs from SLURM
        """
        self.partlist.parse_partlist()
        self.partlist.formate_partlist()
        self.joblist.parse_joblist()
        self.joblist.formate_joblist()

    def partitions_to_db(self):
        """
        Filling in database with actual partitionlist
        """
        for partition in self.partlist.formated_partlist:
            try:
                part_record = Partition.objects.get(name=partition)
                part_record.avail = self.partlist.formated_partlist[partition]['avail']
                part_record.nodes_count = self.partlist.formated_partlist[partition]['nodes_count']
                part_record.nodes_status = self.partlist.formated_partlist[partition]['nodes_status']
                part_record.cpus_status = self.partlist.formated_partlist[partition]['cpus_status']
                part_record.small_nodes_list = self.partlist.formated_partlist[partition]['small_nodes_list']
                part_record.all_nodes_list = ' '.join(self.partlist.formated_partlist[partition]['all_nodes_list'])
                part_record.save()
            except Partition.DoesNotExist:
                Partition.objects.create(**self.partlist.formated_partlist[partition])

    def jobs_to_db(self):
        """
        Clearing old jobs and filling in database with actual jobs
        """
        jobs = Job.objects.all()
        for job in jobs:
            job.delete()

        # write new jobs
        for job in self.joblist.formated_joblist:
            Job.objects.create(**self.oblist.formated_joblist[job])


# debugging part:
# if __name__ == '__main__':
#     j = DbFill()
#     time_start = time.time()
#     j.data_parse()
#     time_parse = time.time()
#     j.partitions_to_db()
#     time_part = time.time()
#     j.jobs_to_db()
#     time_jobs = time.time()
#
#     print(time_parse - time_start)
#     print(time_part - time_parse)
#     print(time_jobs - time_part)
#     print(time_jobs - time_start)
