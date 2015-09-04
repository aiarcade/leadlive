from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf  import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django import forms
from django.http import HttpResponse,HttpResponseRedirect
import json
from lead_platform.models import Student
from lead_platform.models import Staff
from lead_platform.models import Batch
from lead_platform.models import BatchDivision
from lead_platform.models import Subject
from lead_platform.models import SubjectMap
from lead_platform.models import Attendance

from forms import StudentForm 
from forms import StaffForm 
from forms import BatchForm 
from forms import BatchDivisionForm 

from forms import SubjectForm 
from forms import SubjectMapForm


import datetime


def is_lead_admin(user):
    groups=user.groups.filter(name='administration')
    if len(groups)>0:    
        return True
    else:
        return False


class GroupRequiredMixin(object):
    @method_decorator(user_passes_test(is_lead_admin))
    def dispatch(self, *args, **kwargs):
        return super(GroupRequiredMixin, self).dispatch(*args, **kwargs)


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view) 



class AdminDashBoardView( LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'admin_dashboard.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name,{})

########################Students#########################
class AdminStudentsAddView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'students.html'
    
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        form=StudentForm()
        #form.fields['admitted_date'].initial=
        return render(request, self.template_name,{'form':form})
    def post(self, request, *args, **kwargs):
        form=StudentForm(request.POST)
        student = form.save(commit=False)
        user = User.objects.create_user(student.admission_no,student.email,'1111')
        user.first_name=student.name
        user.save()
        group = Group.objects.get(name='students') 
        group.user_set.add(user)
        student.save()
        return HttpResponseRedirect('/admin/students')

class AdminStudentsEditView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'student_edit.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        adm_no=args[0]
        studentObj=Student.objects.filter(admission_no=adm_no)
        form=StudentForm(instance=studentObj[0])
        form.fields['admitted_date'].initial=studentObj[0].admitted_date.strftime('%d/%m/%y')
        #form.fields['uid'].initial='10'
        #form.fields['std_uid'].clean(studentObj[0].id)
        #stud_table=Student.objects.filter(batch_div__batch__status='Live')
        #print form
        
        return render(request, self.template_name,{'form':form,'uid':adm_no})
    def post(self, request, *args, **kwargs):
        try:
            instance = Student.objects.get(admission_no=request.POST['uid']) #aka admission_no
            form=StudentForm(request.POST,instance=instance)
            student = form.save(commit=False)
            student.save()
            msg="Record saved"
        except:
            msg="Unable to process, Please check all values are present"
        return HttpResponse(json.dumps(dict(result=msg)), content_type="application/json")
        
class AdminStudentsEditViewAjax(LoginRequiredMixin,GroupRequiredMixin,View):
        
        #On get it will fill table data
        def get(self, request, *args, **kwargs):
                  
            students=Student.objects.filter(status='Live')
            records=[]
            for record in students:
                batches=record.batchdivision_set.all()
                batch_str=''
                for batch in batches:
                    batch_str=batch_str+batch.getName()+','
                batch_str=batch_str[:-1]
                records.append([record.admission_no,record.reg_no,record.name,batch_str,record.mobile_no,record.address])
            return HttpResponse(json.dumps(dict(data=records)), content_type="application/json")
             
        def post(self, request, *args, **kwargs):
            _admn_no=request.POST['admn_no']
            user_id=Student.objects.filter(admission_no= _admn_no)[0].id
            Student.objects.filter(admission_no= _admn_no).delete()
            User.objects.filter(username=generate_username(user_id,'STUD')).delete()
            return HttpResponse("Record Deleted")
             
###############################staff##############################
class AdminStaffAddView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'staff.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        form=StaffForm()
        return render(request, self.template_name,{'form':form})
    def post(self, request, *args, **kwargs):
        form=StaffForm(request.POST)
        staff = form.save(commit=False)
        user = User.objects.create_user(staff.emp_no,staff.email,'5555')
        user.first_name=staff.name
        user.save()
        group = Group.objects.get(name='staff') 
        group.user_set.add(user)
        staff.save()
        return HttpResponseRedirect('/admin/staff')

class AdminStaffEditView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'staff_edit.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        _emp_no=args[0]
        staffObj=Staff.objects.filter(emp_no=_emp_no)
        #staff=staffObj.values()[0]
        #staff['uid']=staffObj[0].id
        #staff['joined_date']=staffObj[0].joined_date.strftime('%d/%m/%y')
        form=StaffForm(instance=staffObj[0])
      
        return render(request, self.template_name,{'form':form,'uid':_emp_no})
    def post(self, request, *args, **kwargs):
        try:
            instance = Staff.objects.get(emp_no=request.POST['uid']) #aka emp_no
            form=StaffForm(request.POST,instance=instance)
            staff = form.save(commit=False)
            #user = User.objects.create_user(student.admission_no,student.email, 'johnpassword')
            #user.first_name=student.name
            #user.save()
            staff.save()
            msg="Record saved"
        except:
            msg="Unable to process, Please check all values are present"
        return HttpResponse(json.dumps(dict(result=msg)), content_type="application/json")
        
class AdminStaffEditViewAjax(LoginRequiredMixin,GroupRequiredMixin,View):
        
        #On get it will fill table data
        def get(self, request, *args, **kwargs):
                  
            staff=Staff.objects.all()
            records=[]
            for record in staff:
               records.append([record.emp_no,record.name,record.email,record.mobile_no,record.address])
            return HttpResponse(json.dumps(dict(data=records)), content_type="application/json")
             
        def post(self, request, *args, **kwargs):
            _emp_no=request.POST['emp_no']
            user_id=Staff.objects.filter(emp_no= _emp_no)[0]
            print user_id
            Staff.objects.filter(emp_no= _emp_no).delete()
            User.objects.filter(username=generate_username(user_id,'EMP')).delete()
            return HttpResponse("Record Deleted")
             
######################Batch##################################
#this view will work for both batch and division form get and post
class AdminBatchAddView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'batch.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        batch_form=BatchForm()
        div_form=BatchDivisionForm()
        print div_form
        return render(request, self.template_name,{'batch_form':batch_form,'div_form':div_form})
    def post(self, request, *args, **kwargs):
        print request.POST
        if request.POST['etype']=='batch':
            form=BatchForm(request.POST)
            batch = form.save(commit=True)
            return HttpResponseRedirect('/admin/batch')
        if request.POST['etype']=='division':
            form=BatchDivisionForm(request.POST)
            div = form.save(commit=True)
            return HttpResponseRedirect('/admin/batch/#batch-div-add')
            
            
class AdminBatchEditViewAjax(LoginRequiredMixin,GroupRequiredMixin,View):
        
        #On get it will fill table data
        def get(self, request, *args, **kwargs):
                  
            batch=Batch.objects.all()
            records=[]
            for record in batch:
               records.append([record.id,record.name,record.start_date.strftime('%d/%m/%y'),record.end_date.strftime('%d/%m/%y'),record.status])
            return HttpResponse(json.dumps(dict(data=records)), content_type="application/json")
             
        def post(self, request, *args, **kwargs):
            _batch_id=request.POST['bid']
            if self.checkBatchCanBeDeleted(_batch_id):
                Batch.objects.filter(id=_batch_id).delete()
                return HttpResponse("Record Deleted")
            else:
                 return HttpResponse("Unable to delete record, Is any divison assigned to the batch ?")
        def checkBatchCanBeDeleted(self,_id):
            divisions=BatchDivision.objects.filter(batch__id=_id)
            print divisions
            if len(divisions)==0:
                return True
            else:
                return False
            
class AdminBatchEditView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'batch_edit.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        _batch_id=args[0]
        batchObj=Batch.objects.filter(id=_batch_id)
        batch=batchObj.values()[0]
        batch['bid']=batchObj[0].id
        batch['start_date']=batchObj[0].start_date.strftime('%d/%m/%y')
        batch['end_date']=batchObj[0].end_date.strftime('%d/%m/%y')
        batch['etype']='batch'
        form=BatchForm(batch)
        print form
      
        return render(request, self.template_name,{'form':form})
    def post(self, request, *args, **kwargs):
        try:
            instance = Batch.objects.get(id=request.POST['bid'])
            form=BatchForm(request.POST,instance=instance)
            batch = form.save(commit=False)
            #user = User.objects.create_user(student.admission_no,student.email, 'johnpassword')
            #user.first_name=student.name
            #user.save()
            batch.save()
            msg="Record saved"
        except:
            msg="Unable to process, Please check all values are present"
        return HttpResponse(json.dumps(dict(result=msg)), content_type="application/json")

##############Division################################

class AdminDivisionEditView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'division_edit.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        _div_id=args[0]
        divObj=BatchDivision.objects.filter(id=_div_id)
        div=divObj.values()[0]
        div['did']=divObj[0].id
        div['etype']='division'
        div['batch']=divObj[0].batch.id
        form=BatchDivisionForm(instance=divObj[0])
       
      
        return render(request, self.template_name,{'form':form})
    def post(self, request, *args, **kwargs):
        try:
            instance = BatchDivision.objects.get(id=request.POST['did'])
            form=BatchDivisionForm(request.POST,instance=instance)
            print form
            div = form.save(commit=False)
            #user = User.objects.create_user(student.admission_no,student.email, 'johnpassword')
            #user.first_name=student.name
            #user.save()
            div.save()
            msg="Record saved"
        except:
            msg="Unable to process, Please check all values are present"
        return HttpResponse(json.dumps(dict(result=msg)), content_type="application/json")

class AdminDivisionEditViewAjax(LoginRequiredMixin,GroupRequiredMixin,View):
        
        #On get it will fill table data
        def get(self, request, *args, **kwargs):
                  
            div=BatchDivision.objects.all()
            records=[]
            for record in div:
               records.append([record.id,record.name,record.batch.name])
            return HttpResponse(json.dumps(dict(data=records)), content_type="application/json")
             
        def post(self, request, *args, **kwargs):
            _batchdiv_id=request.POST['did']
            if True:#self.checkBatchCanBeDeleted(_batch_id):
                BatchDivision.objects.filter(id=_batchdiv_id).delete()
                return HttpResponse("Record Deleted")
            else:
                 return HttpResponse("Unable to delete record, Is any divison assigned to the batch ?")
        def checkBatchCanBeDeleted(self,_id):
            divisions=BatchDivision.objects.filter(batch__id=_id)
            print divisions
            if len(divisions)==0:
                return True
            else:
                return False

###############Subjects and Maps#####################
class AdminSubjectAddView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'subject.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        sub_form=SubjectForm()
        map_form=SubjectMapForm()
       
        return render(request, self.template_name,{'subject_form':sub_form,'map_form':map_form})
    def post(self, request, *args, **kwargs):
        print request.POST
        if request.POST['etype']=='subject':
            form=SubjectForm(request.POST)
            sub = form.save(commit=False)
            sub.save()
            return HttpResponseRedirect('/admin/subject')
        if request.POST['etype']=='map':
            form=SubjectMapForm(request.POST)
            _map = form.save(commit=False)
            _map.save()
            return HttpResponseRedirect('/admin/subject/')
            
            
class AdminSubjectEditViewAjax(LoginRequiredMixin,GroupRequiredMixin,View):
        
        #On get it will fill table data
        def get(self, request, *args, **kwargs):
                  
            sub=Subject.objects.all()
            records=[]
            for record in sub:
               records.append([record.id,record.name,record.short_name])
            return HttpResponse(json.dumps(dict(data=records)), content_type="application/json")
             
        def post(self, request, *args, **kwargs):
            _sub_id=request.POST['sid']
            if self.checkSubjectCanBeDeleted(_sub_id):
                Subject.objects.filter(id=_sub_id).delete()
                return HttpResponse("Record Deleted")
            else:
                 return HttpResponse("Unable to delete record, Is this assigned to the batch ?")
        def checkSubjectCanBeDeleted(self,_id):
            _map=SubjectMap.objects.filter(subject__id=_id)
            if len(_map)==0:
                return True
            else:
                return False
            
class AdminSubjectEditView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'subject_edit.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        _sub_id=args[0]
        subObj=Subject.objects.filter(id=_sub_id)
        sub=subObj.values()[0]
        sub['sid']=subObj[0].id
        sub['etype']='subject'
        form=SubjectForm(sub)
        
      
        return render(request, self.template_name,{'form':form})
    def post(self, request, *args, **kwargs):
        try:
            instance = Subject.objects.get(id=request.POST['sid'])
            form=SubjectForm(request.POST,instance=instance)
            sub = form.save(commit=False)
            #user = User.objects.create_user(student.admission_no,student.email, 'johnpassword')
            #user.first_name=student.name
            #user.save()
            sub.save()
            msg="Record saved"
        except:
            msg="Unable to process, Please check all values are present"
        return HttpResponse(json.dumps(dict(result=msg)), content_type="application/json")

class AdminSubMapEditView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'subjectmap_edit.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        _map_id=args[0]
        mapObj=SubjectMap.objects.filter(id=_map_id)
        _map=mapObj.values()[0]
        _map['mid']=mapObj[0].id
        _map['etype']='map'
        _map['batch_div']=mapObj[0].batch_div.id
        _map['staff']=mapObj[0].staff.id
        _map['subject']=mapObj[0].subject.id
        form=SubjectMapForm(_map)
        print form
      
        return render(request, self.template_name,{'form':form})
    def post(self, request, *args, **kwargs):
        if True:
            instance = SubjectMap.objects.get(id=request.POST['mid'])
            if self.checkMapCanBeReassigned(request.POST['mid']):
                form=SubjectMapForm(request.POST,instance=instance)
                _map = form.save(commit=False)
                #user = User.objects.create_user(student.admission_no,student.email, 'johnpassword')
                #user.first_name=student.name
                #user.save()
                _map.save()
                msg="Record saved"
            else:
                msg="Unable to modify record, Is any attendance entry present  ?, If you want to reallocate the subject to another staff , create a new allocation"
        else:
            msg="Unable to process, Please check all values are present"
        return HttpResponse(json.dumps(dict(result=msg)), content_type="application/json")
    def checkMapCanBeReassigned(self,_id):
            attendance=Attendance.objects.filter(sub_map__id=_id)
            print attendance
            if len(attendance)==0:
                return True
            else:
                return False


class AdminSubMapEditViewAjax(LoginRequiredMixin,GroupRequiredMixin,View):
        
        #On get it will fill table data
        def get(self, request, *args, **kwargs):
                  
            _map=SubjectMap.objects.filter(batch_div__batch__status='Live')
            records=[]
            for record in _map:
               records.append([record.id,record.subject.name,record.staff.name,record.batch_div.getName()])
            return HttpResponse(json.dumps(dict(data=records)), content_type="application/json")
             
        def post(self, request, *args, **kwargs):
            _map_id=request.POST['mid']
            if self.checkMapCanBeDeleted(_map_id):
                SubjectMap.objects.filter(id=_map_id).delete()
                return HttpResponse("Record Deleted")
            else:
                 return HttpResponse("Unable to delete record, Is any attendance entry present  ?, If you want to reallocate the subject to another staff , create a new allocation ")
        def checkMapCanBeDeleted(self,_id):
            attendance=Attendance.objects.filter(sub_map__id=_id)
            print attendance
            if len(attendance)==0:
                return True
            else:
                return False




