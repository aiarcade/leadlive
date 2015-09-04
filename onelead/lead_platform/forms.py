from django import forms
from .widgets import MultiSelectWidget

from lead_platform.models import Student
from lead_platform.models import Staff
from lead_platform.models import BatchDivision
from lead_platform.models import Batch
from lead_platform.models import SubjectMap
from lead_platform.models import Subject
import datetime


STATUS_CHOICES = (
    ('0', '0'),
    ('1', '1'),
    ('0.5','0.5'),
	
)
class AttendanceForm(forms.ModelForm):
	date=forms.DateField(input_formats=DATE_FRMT,initial=datetime.date.today().strftime('%d/%m/%y'))
        
    	status_of_student = forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect)
	class Meta:
		model = Attendance 
        	fields = "__all__" 
