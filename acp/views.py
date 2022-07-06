from django.shortcuts import render, get_object_or_404

from .models import Partition, Job
from . import dbfill


def home(request):
    """Home page for acp app"""
    # refresh_db = dbfill.DbFill()
    # refresh_db.partitions_to_db()
    # refresh_db.jobs_to_db()
    partitions = Partition.objects.all().order_by('name')
    running_jobs = Job.objects.filter(job_condition='R').order_by('jobid')

    # defining list of allocated nodes
    allocated_nodes = []
    for job in running_jobs:
        if job.nodes.strip('n').isdigit():
            allocated_nodes.append(job.nodes.strip('n'))
        else:
            node_start = int(job.nodes.strip('n[]').split('-')[0])
            node_fin = int(job.nodes.strip('n[]').split('-')[1])
            allocated_nodes += [str(num) for num in range(node_start, node_fin + 1)]

    context = {'partitions': partitions, 'allocated_nodes': allocated_nodes}
    return render(request, 'acp/home.html', context)


def jobs(request):
    """Page with actual job list"""
    # refresh_db = dbfill.DbFill()
    # refresh_db.jobs_to_db()
    jobs = Job.objects.all().order_by('jobid')
    context = {'jobs': jobs}
    return render(request, 'acp/jobs.html', context)
