import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onelead.settings")
import random
import django
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
django.setup()


from lead_platform.models import Student
from lead_platform.models import Staff

from datetime import datetime 






User.objects.all().delete() 
Group.objects.all().delete() 


newgroup = Group.objects.create(name='administration')
newgroup.save()
user = User.objects.create_user('onelead','onelead@lead.ac.in','pwdadmin')
user.first_name='One Lead admin' 
user.save()
group = Group.objects.get(name='administration') 
group.user_set.add(user)


newgroup = Group.objects.create(name='students')
newgroup.save()

newgroup = Group.objects.create(name='staff')
newgroup.save()

s_group = Group.objects.get(name='students') 
e_group = Group.objects.get(name='staff') 


for student in Student.objects.all():
    print 'creating user',student
    user = User.objects.create_user(student.reg_no,student.email,'1111')
    user.first_name=student.name
    user.save()
    s_group.user_set.add(user)
    

for staff in Staff.objects.all():
    user=User.objects.filter(email=staff.email)
    print 'creating user',staff
    user = User.objects.create_user(staff.emp_no,staff.email,'5555')
    user.first_name=staff.name
    user.save()
    e_group.user_set.add(user)
