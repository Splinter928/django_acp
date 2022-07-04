import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_acp.settings'
import django

django.setup()

import json
from acp.models import Partition, Job


class DbFill:

    def __init__(self):
        self.part_list = {}
        self.jobs_list = {}

    def partitions_to_db(self):
        """
        Fill in database with actual partitionlist
        """
        # read partition data from JSON, which already parsed
        with open('acp/data/partition_list.json') as pl:
            self.part_list = json.load(pl)

        for partition in self.part_list:
            try:
                part_record = Partition.objects.get(name=partition)
                part_record.name = self.part_list[partition]['name']
                part_record.avail = self.part_list[partition]['avail']
                part_record.nodes_count = self.part_list[partition]['nodes_count']
                part_record.nodes_status = self.part_list[partition]['nodes_status']
                part_record.cpus_status = self.part_list[partition]['cpus_status']
                part_record.small_nodes_list = self.part_list[partition]['small_nodes_list']
                part_record.all_nodes_list = ' '.join(self.part_list[partition]['all_nodes_list'])
                part_record.save()
            except Partition.DoesNotExist:
                Partition.objects.create(**self.part_list[partition])

    def jobs_to_db(self):
        """
        Fill in database with actual jobs
        """
        # read jobs data from JSON, which already parsed
        with open('acp/data/job_list.json') as pl:
            self.jobs_list = json.load(pl)

        # clear current jobs
        jobs = Job.objects.all()
        for job in jobs:
            Job.objects.filter(jobid=job.jobid).delete()

        # write new jobs
        for job in self.jobs_list:
            Job.objects.create(**self.jobs_list[job])


if __name__ == '__main__':
    # part for debugging
    j = DbFill()
    # j.partitions_to_db()
    j.jobs_to_db()
