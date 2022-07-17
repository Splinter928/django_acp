from django.db import models


class Partition(models.Model):
    """
    Model representing a partition.
    """

    # Fields
    name = models.CharField(max_length=100, unique=True)
    avail = models.CharField(max_length=10)
    nodes_count = models.IntegerField()
    nodes_status = models.CharField(max_length=100)
    cpus_status = models.CharField(max_length=100)
    small_nodes_list = models.TextField()
    all_nodes_list = models.TextField()

    # Metadata
    class Meta:
        ordering = ["name"]

    # Methods
    def __str__(self):
        """
        String representation for the Model object.
        """
        return str(self.name) + ': ' + str(self.small_nodes_list)


class Job(models.Model):
    """
    Model representing a job.
    """

    # Fields
    jobid = models.CharField(max_length=20, unique=True)
    partition = models.CharField(max_length=100)
    job_name = models.CharField(max_length=200)
    user = models.CharField(max_length=20)
    job_condition = models.CharField(max_length=5)
    calc_time = models.CharField(max_length=20)
    num_nodes = models.IntegerField()
    num_cpus = models.IntegerField()
    project = models.CharField(max_length=20)
    nodes = models.TextField()

    # Metadata
    class Meta:
        ordering = ["-job_condition", "jobid"]

    # Methods
    def __str__(self):
        """
        String representation for the Model object.
        """
        return f"[{self.job_condition}] {self.jobid}: {self.job_name} - {self.user}"


class Node(models.Model):
    """
    Model representing a node.
    """

    # Fields
    node = models.CharField(max_length=20, unique=True)
    partition = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    cpus = models.IntegerField()
    cpus_status = models.CharField(max_length=100)
    memory = models.IntegerField()
    tmp = models.IntegerField()

    # Metadata
    class Meta:
        ordering = ["node"]

    # Methods
    def __str__(self):
        """
        String representation for the Model object.
        """
        return str(self.node) + ': ' + str(self.status)
