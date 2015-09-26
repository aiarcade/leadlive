import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "onelead.settings")
import random
from lead_platform.models import *
import django
django.setup()
from datetime import date
import datetime

LeaveRequest.objects.all().delete()


