from connection_settings import Settings
from partitionlist import PartitionList
from joblist import JobList


class Parser:
    def __init__(self):
        self.settings = Settings()
        self.partlist = PartitionList(self)
        self.joblist = JobList(self)

    def data_parse(self):
        self.partlist.prepare_json_partlist()
        self.joblist.parse_joblist()
        self.joblist.formate_joblist()
        self.joblist.json_jobfilecreation()


if __name__ == '__main__':
    parser = Parser()
    parser.data_parse()
