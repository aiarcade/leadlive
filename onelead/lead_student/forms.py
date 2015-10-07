from django import forms

from lead_admin.widgets import MultiSelectWidget

from lead_platform.models import Student
from lead_platform.models import Staff
from lead_platform.models import BatchDivision
from lead_platform.models import Batch
from lead_platform.models import SubjectMap
from lead_platform.models import Subject
from lead_platform.models import LeaveRequest
import datetime
from datetime import date

GENDER_CHOICES = (
    ('M', 'M'),
    ('F', 'F'),
    
)
SESSION_CHOICES= (
('1', '1'),
('2', '2'),
('3', '3'),
('4', '4'))
STATUS_CHOICES = (
    ('Live', 'Live'),
    ('Finished', 'Finished'),
    
)
DATE_FRMT=['%d/%m/%y']

class LeaveRequestForm(forms.ModelForm):
	start_date=forms.DateTimeField(initial=date.today())
	end_date=forms.DateTimeField(initial=date.today())
	
	class Meta:
		model = LeaveRequest 
        	exclude=('leave_status',)



	
