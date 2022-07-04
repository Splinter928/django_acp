from django.shortcuts import render, get_object_or_404

from .models import Partition, Job
from . import dbfill


def home(request):
    """Home page for acp app"""
    refresh_db = dbfill.DbFill()
    refresh_db.partitions_to_db()
    partitions = Partition.objects.all().order_by('name')
    context = {'partitions': partitions}
    return render(request, 'acp/home.html', context)

def jobs(request):
    """Page with actual job list"""
    refresh_db = dbfill.DbFill()
    refresh_db.jobs_to_db()
    jobs = Job.objects.all().order_by('jobid')
    context = {'jobs': jobs}
    return render(request, 'acp/jobs.html', context)

