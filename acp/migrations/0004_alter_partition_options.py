# Generated by Django 4.0.4 on 2022-06-28 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acp', '0003_rename_nodes_list_partition_all_nodes_list_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='partition',
            options={'ordering': ['-name']},
        ),
    ]
