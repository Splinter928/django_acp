# Generated by Django 4.0.4 on 2022-07-04 17:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acp', '0007_rename_small_nodes_list_job_nodes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['job_condition', 'calc_time']},
        ),
    ]
