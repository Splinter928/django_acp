# Generated by Django 4.0.4 on 2022-07-04 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acp', '0008_alter_job_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='job',
            options={'ordering': ['-job_condition', '-calc_time']},
        ),
        migrations.AlterField(
            model_name='job',
            name='calc_time',
            field=models.CharField(max_length=20),
        ),
    ]
