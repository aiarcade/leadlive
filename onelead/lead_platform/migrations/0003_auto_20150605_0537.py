# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead_platform', '0002_timetable_timetableslots'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='timetable',
            name='date',
        ),
        migrations.RemoveField(
            model_name='timetable',
            name='slot_no',
        ),
        migrations.AddField(
            model_name='timetable',
            name='end_date_time',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timetable',
            name='sid',
            field=models.CharField(max_length=100, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='timetable',
            name='start_date_time',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
