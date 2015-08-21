from django import forms

from .widgets import MultiSelectWidget

from lead_platform.models import Student
from lead_platform.models import Staff
from lead_platform.models import BatchDivision
from lead_platform.models import Batch
from lead_platform.models import SubjectMap
from lead_platform.models import Subject
import datetime

GENDER_CHOICES = (
    ('M', 'M'),
    ('F', 'F'),
    
)
STATUS_CHOICES = (
    ('Live', 'Live'),
    ('Finished', 'Finished'),
    
)
DATE_FRMT=['%d/%m/%y']

class StudentForm(forms.ModelForm):
   
    gender = forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect)
    admitted_date=forms.DateField(initial=datetime.date.today().strftime('%Y-%m-%d'))
    #uid = forms.CharField(widget=forms.widgets.HiddenInput(),initial='0')
    class Meta:
        model = Student # 
        #fields = "__all__"
        exclude=('status',)
    def clean_admission_no(self):
        adm_no = self.cleaned_data['admission_no']
        return adm_no.replace(" ","")
        
class StaffForm(forms.ModelForm):
   
    gender = forms.ChoiceField(choices=GENDER_CHOICES,widget=forms.RadioSelect)
    joined_date=forms.DateField(initial=datetime.date.today().strftime('%Y-%m-%d'))
    uid = forms.CharField(widget=forms.widgets.HiddenInput(),initial='0')
    class Meta:
        model = Staff # 
        fields = "__all__" 
        exclude=('status',) 
    def clean_emp_no(self):
        emp_no = self.cleaned_data['emp_no']
        return emp_no.replace(" ","")
        
class BatchForm(forms.ModelForm):
    
    start_date=forms.DateField(input_formats=DATE_FRMT,initial=datetime.date.today().strftime('%d/%m/%y'))
    end_date=forms.DateField(input_formats=DATE_FRMT,initial=datetime.date.today().strftime('%d/%m/%y'))
    bid = forms.CharField(widget=forms.widgets.HiddenInput(),initial='0')
    etype = forms.CharField(widget=forms.widgets.HiddenInput(),initial='batch')
    status = forms.ChoiceField(choices=STATUS_CHOICES,widget=forms.RadioSelect)
    class Meta:
        model = Batch # 
        fields = "__all__" 
        
class BatchDivisionForm(forms.ModelForm):
    did = forms.CharField(widget=forms.widgets.HiddenInput(),initial='0')
    etype = forms.CharField(widget=forms.widgets.HiddenInput(),initial='division')
    students =  forms.ModelMultipleChoiceField(widget=MultiSelectWidget, queryset=Student.objects.filter(status='Live'))
    class Meta:
        model = BatchDivision # 
        fields = "__all__" 


class SubjectForm(forms.ModelForm):
    
    sid = forms.CharField(widget=forms.widgets.HiddenInput(),initial='0')
    etype = forms.CharField(widget=forms.widgets.HiddenInput(),initial='subject')
    class Meta:
        model = Subject # 
        fields = "__all__" 
        
class SubjectMapForm(forms.ModelForm):
    mid = forms.CharField(widget=forms.widgets.HiddenInput(),initial='0')
    etype = forms.CharField(widget=forms.widgets.HiddenInput(),initial='map')
    class Meta:
        model = SubjectMap # 
        #fields = "__all__" 
        exclude=('status',) 


