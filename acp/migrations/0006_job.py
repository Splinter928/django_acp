# Generated by Django 4.0.4 on 2022-07-04 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acp', '0005_alter_partition_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('jobid', models.CharField(max_length=20, unique=True)),
                ('partition', models.CharField(max_length=100)),
                ('job_name', models.CharField(max_length=200)),
                ('user', models.CharField(max_length=20)),
                ('job_condition', models.CharField(max_length=5)),
                ('calc_time', models.TimeField()),
                ('num_nodes', models.IntegerField()),
                ('num_cpus', models.IntegerField()),
                ('project', models.CharField(max_length=20)),
                ('small_nodes_list', models.TextField()),
            ],
            options={
                'ordering': ['calc_time', 'job_name'],
            },
        ),
    ]
