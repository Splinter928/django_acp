# Generated by Django 4.0.4 on 2022-06-27 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acp', '0002_rename_partitions_partition'),
    ]

    operations = [
        migrations.RenameField(
            model_name='partition',
            old_name='nodes_list',
            new_name='all_nodes_list',
        ),
        migrations.AddField(
            model_name='partition',
            name='cpus_status',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partition',
            name='nodes_status',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='partition',
            name='small_nodes_list',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='partition',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
