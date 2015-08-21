import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onelead.settings")
import random
import django
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
django.setup()



group=Group.objects.filter(name='administration')
if len(group)==0: # is any admin group
    newgroup = Group.objects.create(name='administration')
user = User.objects.create_user('admin','onelead@lead.ac.in','pwdadmin')
user.first_name='One Lead admin' 
user.save()
group = Group.objects.get(name='administration') 
group.user_set.add(user)

