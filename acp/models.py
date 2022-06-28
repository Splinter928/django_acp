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
        String for representing the Model object.
        """
        return str(self.name) + ': ' + str(self.small_nodes_list)
