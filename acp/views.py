from django.shortcuts import render, get_object_or_404

from .models import Partition
from . import dbfill


def home(request):
    """Home page for acp app"""
    refresh_db = dbfill.DbFill()
    refresh_db.json_to_db()
    partitions = Partition.objects.all().order_by('name')
    context = {'partitions': partitions}
    return render(request, 'acp/home.html', context)
