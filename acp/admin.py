from django.contrib import admin
from .models import Partition, Job, Node

admin.site.register(Partition)
admin.site.register(Job)
admin.site.register(Node)
