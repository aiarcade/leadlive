# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('slot_no', models.CharField(max_length=2)),
                ('status_of_student', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Attendance',
                'verbose_name_plural': 'Attendance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('start_date', models.DateField(verbose_name=b'Started Date (dd/mm/yy)')),
                ('end_date', models.DateField(verbose_name=b'Finishing Date (dd/mm/yy)')),
                ('status', models.CharField(default=b'Live', max_length=10)),
            ],
            options={
                'verbose_name': 'Batch',
                'verbose_name_plural': 'Batches',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BatchDivision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('batch', models.ForeignKey(to='lead_platform.Batch')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('emp_no', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=1)),
                ('address', models.CharField(max_length=200)),
                ('emergency_phone_no', models.CharField(max_length=20)),
                ('mobile_no', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('education_history', models.CharField(max_length=200)),
                ('joined_date', models.DateField(verbose_name=b'joined_date')),
                ('emp_type', models.CharField(max_length=20)),
                ('teaching_experience', models.CharField(max_length=5, null=True)),
                ('industrial_experience', models.CharField(max_length=5, null=True)),
                ('status', models.CharField(default=b'Live', max_length=10)),
            ],
            options={
                'verbose_name': 'Staff',
                'verbose_name_plural': 'Staffs',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('admission_no', models.CharField(max_length=20, verbose_name=b'Admission No')),
                ('reg_no', models.CharField(max_length=20, null=True, verbose_name=b'University Reg No')),
                ('name', models.CharField(max_length=200)),
                ('gender', models.CharField(max_length=1)),
                ('address', models.CharField(max_length=200)),
                ('emergency_phone_no', models.CharField(max_length=20)),
                ('mobile_no', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=50)),
                ('parents', models.CharField(max_length=200)),
                ('education_history', models.CharField(max_length=200)),
                ('admitted_date', models.DateField(verbose_name=b'Admitted Date')),
                ('status', models.CharField(default=b'Live', max_length=10)),
            ],
            options={
                'verbose_name': 'Student',
                'verbose_name_plural': 'Students',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('short_name', models.CharField(max_length=10)),
            ],
            options={
                'verbose_name': 'Subject',
                'verbose_name_plural': 'Subjects',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubjectMap',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.CharField(default=b'Live', max_length=10)),
                ('batch_div', models.ForeignKey(to='lead_platform.BatchDivision')),
                ('staff', models.ForeignKey(to='lead_platform.Staff')),
                ('subject', models.ForeignKey(to='lead_platform.Subject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='batchdivision',
            name='students',
            field=models.ManyToManyField(to='lead_platform.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendance',
            name='student',
            field=models.ForeignKey(to='lead_platform.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='attendance',
            name='sub_map',
            field=models.ForeignKey(to='lead_platform.SubjectMap'),
            preserve_default=True,
        ),
    ]
