import os, sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_acp.settings'
import django

django.setup()

import json
from acp.models import Partition


class DbFill:
    def __init__(self):
        self.part_list = {}

    def json_to_db(self):
        with open('acp/data/partition_list.json') as pl:
            self.part_list = json.load(pl)

        for partition in self.part_list:
            all_nodes = self.part_list[partition]['ALLNODES']
            try:
                part_record = Partition.objects.get(name=partition)
                part_record.name = partition
                part_record.avail = self.part_list[partition]['AVAIL']
                part_record.nodes_count = self.part_list[partition]['NODECOUNT']
                part_record.nodes_status = self.part_list[partition]['NODESTATUS']
                part_record.cpus_status = self.part_list[partition]['CPUS']
                part_record.small_nodes_list = self.part_list[partition]['NODELIST']
                part_record.all_nodes_list = ' '.join(self.part_list[partition]['ALLNODES'])
                part_record.save()
            except Partition.DoesNotExist:
                Partition.objects.create(
                    name=partition,
                    avail=self.part_list[partition]['AVAIL'],
                    nodes_count=self.part_list[partition]['NODECOUNT'],
                    nodes_status=self.part_list[partition]['NODESTATUS'],
                    cpus_status=self.part_list[partition]['CPUS'],
                    small_nodes_list=self.part_list[partition]['NODELIST'],
                    all_nodes_list=' '.join(self.part_list[partition]['ALLNODES'])
                )


if __name__ == '__main__':
    j = DbFill()
    j.json_to_db()
