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
        with open('data/partition_list.json') as pl:
            self.part_list = json.load(pl)

        for partition in self.part_list:
            part_record = Partition(
                name=partition,
                avail=self.part_list[partition]['AVAIL'],
                nodes_count=self.part_list[partition]['NODECOUNT'],
                nodes_status=self.part_list[partition]['NODESTATUS'],
                cpus_status=self.part_list[partition]['CPUS'],
                small_nodes_list=self.part_list[partition]['NODELIST'],
                all_nodes_list=self.part_list[partition]['ALLNODES'],
            )
            part_record.save()


j = DbFill()
j.json_to_db()
