from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.views.generic import View
from lead_platform.models import SubjectMap
from lead_platform.models import Student
from lead_platform.models import Staff
from lead_platform.models import Attendance
from lead_platform.models import LeaveRequest
from lead_platform.models import Mentorship
from .forms import LeaveRequestForm
from datetime import date
import datetime
import json
from django.views.decorators.csrf  import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.views.generic.list import ListView
from django.utils import timezone



class StudentDashBoardView(View):
    template_name = 'dashboard_student.html'
    
    def get(self, request, *args, **kwargs):
        _id=request.session['_id']
        _student=Student.objects.filter(admission_no=_id)[0]
        form=LeaveRequestForm(initial={'student': _student})
        today = date.today()
        year=today.year
        day=today.day
        month=today.month
        hour=1
        
        return render(request, self.template_name,{'form':form,'student':_student})

    def post(self, request, *args, **kwargs):

        form=LeaveRequestForm(request.POST)
	leaverequest=form.save(commit=True)
	return HttpResponseRedirect('/students')
	
