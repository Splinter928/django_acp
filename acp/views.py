from django.shortcuts import render, redirect, get_object_or_404
from django.db import OperationalError
from .models import Partition, Job, Node
from .parse_data.dbfill import DbFill


def home(request):
    """Home page for acp app with all nodes status"""
    db_updater = DbFill()
    db_updater.filling_db()

    try:
        partitions = Partition.objects.all().order_by('name')
        current_nodes = Node.objects.all()

        nodes_status = {}
        for cnode in current_nodes:
            nodes_status[cnode.node.strip('n')] = cnode.status

        all_nodes_status = db_updater.partlist.formated_summary["NODES(A/I/O/T)"].split('/')
        all_cpus_status = db_updater.partlist.formated_summary["CPUS(A/I/O/T)"].split('/')

        context = {
            'partitions': partitions,
            'cur_nodes': nodes_status,
            'nodes': all_nodes_status,
            'cpus': all_cpus_status,
        }
        return render(request, 'acp/home.html', context)

    except OperationalError:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def jobs(request):
    """Page with actual job list"""
    db_updater = DbFill()
    db_updater.filling_db()

    try:
        jobs = Job.objects.all().order_by('-job_condition', 'jobid')
        context = {'jobs': jobs}
        return render(request, 'acp/jobs.html', context)
    except OperationalError:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


def nodes(request):
    """Page with actual nodes information"""
    db_updater = DbFill()
    db_updater.filling_db()

    try:
        nodes = Node.objects.all()
        context = {'nodelist': nodes}
        return render(request, 'acp/nodes.html', context)
    except OperationalError:
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
