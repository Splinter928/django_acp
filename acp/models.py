from django.db import models


class Partition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    avail = models.CharField(max_length=10)
    nodes_count = models.IntegerField()
    nodes_status = models.CharField(max_length=100)
    cpus_status = models.CharField(max_length=100)
    small_nodes_list = models.TextField()
    all_nodes_list = models.TextField()

    def __str__(self):
        """Returns string representation of the model"""
        return str(self.name) + ':' + str(self.avail)
