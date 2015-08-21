# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lead_platform', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('slot_no', models.CharField(max_length=2)),
                ('sub_map', models.ForeignKey(to='lead_platform.SubjectMap')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TimeTableSlots',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('slot_no', models.CharField(max_length=2)),
                ('batch_div', models.ManyToManyField(to='lead_platform.BatchDivision')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
