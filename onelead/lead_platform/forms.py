from django import forms
from lead_admin.widgets import MultiSelectWidget

from lead_platform.models import Student
from lead_platform.models import Staff
from lead_platform.models import BatchDivision
from lead_platform.models import Batch
from lead_platform.models import SubjectMap
from lead_platform.models import Subject
from lead_platform.models import LeaveRequest
from lead_platform.models import Attendance
import datetime


STATUS_CHOICES = (
    ('0', '0'),
    ('1', '1'),
    ('0.5','0.5'),
	
)
LEAVE_STATUS=(
    ('0', '0'),
    ('1', '1'),

)
class AttendanceForm(forms.ModelForm):
	date=forms.DateField(initial=datetime.date.today().strftime('%d/%m/%y'))
        
    	status_of_student = forms.ChoiceField(choices=STATUS_CHOICES,widget=forms.RadioSelect)
	class Meta:
		model = Attendance 
        	fields = "__all__" 


class LeaveAcceptForm(forms.ModelForm):
	start_date=forms.DateField(initial=datetime.date.today().strftime('%d/%m/%y'))
	end_date=forms.DateField(initial=datetime.date.today().strftime('%d/%m/%y'))
	leave_status = forms.ChoiceField(choices=LEAVE_STATUS,widget=forms.RadioSelect)
	class Meta:
		model = LeaveRequest 
        	fields = "__all__" 

