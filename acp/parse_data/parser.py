from . import connection_settings, partitionlist, joblist


class Parser:
    def __init__(self):
        self.settings = connection_settings.Settings()
        self.partlist = partitionlist.PartitionList(self)
        self.joblist = joblist.JobList(self)

    def data_parse(self):
        self.partlist.prepare_json_partlist()
        self.joblist.prepare_json_joblist()


if __name__ == '__main__':
    parser = Parser()
    parser.data_parse()
