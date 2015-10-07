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

from datetime import date

import datetime


from lead_platform.models import Student
from lead_platform.models import Staff
from lead_platform.models import Batch
from lead_platform.models import BatchDivision
from lead_platform.models import Subject
from lead_platform.models import SubjectMap
from lead_platform.models import Attendance
from lead_platform.models import Mentorship
from lead_platform.models import LeaveRequest
from lead_student.forms import LeaveRequestForm             
from lead_platform.forms import LeaveAcceptForm

from lead_platform.models import OdList

from lead_platform.forms import OdForm
from forms import StudentForm 
from forms import StaffForm 
from forms import BatchForm 
from forms import BatchDivisionForm 

from forms import SubjectForm 
from forms import SubjectMapForm
from forms import MentorshipForm

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
            User.objects.filter(username=_admn_no).delete()
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
            User.objects.filter(username=_emp_no).delete()
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


############### Mentors #####################

class MentorAddView(LoginRequiredMixin,GroupRequiredMixin,View):
	template_name='mentor_add.html'
	def get(self, request, *args, **kwargs):
		form=MentorshipForm
		return render(request, self.template_name,{'form':form})
	def post(self, request, *args, **kwargs):
        	
        	
            	form=MentorshipForm(request.POST)
            	mentorship = form.save(commit=True)
            	return HttpResponseRedirect('/admin/mentors')


class AdminMentorEditViewAjax(LoginRequiredMixin,GroupRequiredMixin,View):
        
        #On get it will fill table data
        def get(self, request, *args, **kwargs):
                  
            mentor=Mentorship.objects.all()
            records=[]
            for record in mentor:
               records.append([record.id,record.name,record.staff.name])
            return HttpResponse(json.dumps(dict(data=records)), content_type="application/json")
             
        def post(self, request, *args, **kwargs):
            _mentor_id=request.POST['mid']
	    
            if True:
		Mentorship.objects.filter(id=_mentor_id).delete()
                return HttpResponse("Record Deleted")
            else:
                return HttpResponse("Unable to delete record")

        
class AdminMentorEditView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'mentor_edit.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        _mentor_id=args[0]
        mentObj=Mentorship.objects.filter(id=_mentor_id)
        mentor=mentObj.values()[0]
        mentor['mid']=mentObj[0].id
       	mentor['batch']=mentObj[0].batch.id
        mentor['staff']=mentObj[0].staff.id
	
        form=MentorshipForm(instance=mentObj[0])
        print form
      
        return render(request, self.template_name,{'form':form})
    def post(self, request, *args, **kwargs):
        try:
            instance = Mentorship.objects.get(id=request.POST['mid'])
            form=MentorshipForm(request.POST,instance=instance)
            mentor = form.save(commit=False)
            
            mentor.save()
            msg="Record saved"
        except:
            msg="Unable to process, Please check all values are present"
        return HttpResponse(json.dumps(dict(result=msg)), content_type="application/json")

############### Attendance #####################


class AdminAttendanceView( LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'attendance_dashboard.html'
    
    def get(self, request, *args, **kwargs):
        _divs=BatchDivision.objects.filter(batch__status='Live')
        return render(request, self.template_name,{'divs':_divs})

    def post(self, request, *args, **kwargs):
        pass

class AdminAttendanceSubView(LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'attendance_subs.html'
    
    def get(self, request, *args, **kwargs):
        
        _sub_maps=SubjectMap.objects.filter(batch_div__id=int(args[0]))
        today = date.today()
        year=today.year
        day=today.day
        month=today.month
        hour=1
        sub_maps={'sub_maps':_sub_maps,'year':year,'month':month,'day':day,'hour':hour}
        return render(request, self.template_name,sub_maps)

    def post(self, request, *args, **kwargs):
        pass


class AdminAttendanceAjaxView(View):
    template_name = 'attendance_admin.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        _r_map=args[0]
        _slot=args[4]
        _date=date(int(args[1]),int(args[2]),int(args[3]))
        _sub_map=SubjectMap.objects.filter(id=_r_map)[0]
        students=Student.objects.filter(batchdivision=_sub_map.batch_div)
        _attendance=[]
        empty_attendance=[]
        marked_on_theday =Attendance.objects.filter(date=_date,sub_map__batch_div=_sub_map.batch_div).values('slot_no','sub_map__subject__name','sub_map').distinct()
        print marked_on_theday
        
        
        for _student in students:
            attendance=Attendance.objects.filter(date=_date,sub_map=_sub_map,student=_student,slot_no=_slot)
            if len(attendance)>0:
                _attendance.append({'name':_student.name,'id':_student.admission_no,'status':attendance[0].status_of_student,'roll':_student.reg_no})
            else:
                empty_attendance.append({'name':_student.name,'id':_student.admission_no,'status':'P','roll':_student.reg_no})
        free_slots=[]
        
        #TODO fetch the total number of slots(range of i) from a configuration table,
        
        for i in range(1,5):
            flag=0
            for slot in marked_on_theday:
                #if its is a free slot on the day 
                
                if str(i)==slot['slot_no'] :
                    flag=1
                    break
            if flag==0:
                free_slots.append(i)
        for slot in marked_on_theday:
            #or slot belongs to already exist  entry of the map
            if slot['sub_map']==int(_r_map):
                free_slots.append(int(slot['slot_no']))
            
        if len(_attendance)>0 and len(empty_attendance)==0: # it is marked early
            return render(request, self.template_name,{'attendance_data':_attendance,'marked':marked_on_theday,
            'map':_r_map,'r_year':args[1],'r_month':args[2],'r_date':args[3],'slot':int(_slot),'sub':_sub_map.subject.name,'freeslots':free_slots})
        if len(_attendance)==0 and len(empty_attendance)>0: # it is a new request
            return render(request, self.template_name,{'attendance_data':empty_attendance,'marked':marked_on_theday,'map':_r_map,
             'map':_r_map,'r_year':args[1],'r_month':args[2],'r_date':args[3],'slot':int(_slot),'sub':_sub_map.subject.name,'freeslots':free_slots})
        if len(_attendance)>0 and len(empty_attendance)>0: # partial mark
            return render(request, self.template_name,{'attendance_data':_attendance+empty_attendance,'marked':marked_on_theday,'map':_r_map,
             'map':_r_map,'r_year':args[1],'r_month':args[2],'r_date':args[3],'slot':int(_slot),'sub':_sub_map.subject.name,'freeslots':free_slots})
    	
    
    def post(self, request, *args, **kwargs):
        
        data=json.loads(request.POST['attn_data'])
        r_date= datetime.datetime.strptime(str(request.POST['date']), '%d/%m/%Y').date()
        r_slot=request.POST['slot']
        r_map=request.POST['map']
        attn_on_theday=Attendance.objects.filter(date=r_date,sub_map=r_map,slot_no=r_slot)
        if len(attn_on_theday)>0:
            
            for key,attendance in data.items():
                attendance_marked=Attendance.objects.filter(date=r_date,sub_map=r_map,student__admission_no=key,slot_no=r_slot)
                
                if len(attendance_marked)>0:
                    
                    attendance_marked[0].status_of_student=attendance['status']
                    attendance_marked[0].sub_map=SubjectMap.objects.filter(id=int(r_map))[0]
                    attendance_marked[0].save()
                else:
                    _attn=Attendance()
                    _attn.date=r_date
                    _attn.slot_no=r_slot
                    _attn.student=Student.objects.filter(admission_no=attendance['adm_no'])[0]
                    _attn.status_of_student=attendance['status']
                    _attn.sub_map=SubjectMap.objects.filter(id=int(r_map))[0]
                    _attn.save()
            return HttpResponse("Record Modified")
                
        else:
           
            for key,attendance in data.items():
                
                _attn=Attendance()
                _attn.date=r_date
                _attn.slot_no=r_slot
                _attn.student=Student.objects.filter(admission_no=attendance['adm_no'])[0]
                _attn.status_of_student=attendance['status']
                _attn.sub_map=SubjectMap.objects.filter(id=int(r_map))[0]
                _attn.save()
            return HttpResponse("New record Saved")
                
        
        return HttpResponse("Saved")


class AdminAttendanceDeleteAjaxView(View):
        
        
        def get(self, request, *args, **kwargs):
            dt_from=request.GET['dtfrom'][0:10]
            dt_to=request.GET['dtto'][0:10]
            attendance_on_range=Attendance.objects.filter(date__range=[dt_from,dt_to]).values('slot_no','sub_map__subject__name','sub_map__id','date').distinct()
            
            records=[]
            for record in attendance_on_range:
               records.append([record['date'].strftime('%d/%m/%y'),record['slot_no'],record['sub_map__subject__name'],str(record['sub_map__id'])])
            return HttpResponse(json.dumps(dict(data=records)), content_type="application/json")
             
        def post(self, request, *args, **kwargs):
            _date=datetime.datetime.strptime(str(request.POST['date']), '%d/%m/%y').date()
            _slot=request.POST['slot']
            Attendance.objects.filter(date=_date,slot_no=_slot).delete()
            return HttpResponse("Record Deleted")
 

#################################################Leave##########################################
class AdminConfirmLeaveView(View):
    template_name = 'leave_view.html'
    def get(self, request, *args, **kwargs):
               
        return render(request, self.template_name)
class AdminConfirmLeaveEditView(View):    
    def get(self, request, *args, **kwargs):
      	today = date.today()
        leave=LeaveRequest.objects.filter(start_date=today)
	records=[]
        for record in leave:
       			records.append([record.id,record.student.name,record.mentor.name,record.start_date.strftime('%d/%m/%y'),record.end_date.strftime('%d/%m/%y'),record.session,record.reason])
        return HttpResponse(json.dumps(dict(data=records)),content_type="application/json")
    def post(self, request, *args, **kwargs):
            _mentor_id=request.POST['id']
	    if True:
		LeaveRequest.objects.filter(id=_mentor_id).delete()
                return HttpResponse("Record Deleted")
            else:
                return HttpResponse("Unable to delete record")	

class AdminLeaveEditView(View):
    template_name = 'leave_admin_edit.html'
    
    def get(self, request, *args, **kwargs):
	_mentor_id=args[0]
        mentObj=LeaveRequest.objects.filter(id=_mentor_id)
        mentor=mentObj.values()[0]
        mentor['mentor']=mentObj[0].mentorship.id
	mentor['student']=mentObj[0].student.id
        form=LeaveAcceptForm(mentor)
        print form
    	return render(request, self.template_name,{'form':form})
    def post(self, request, *args, **kwargs):
        try:
            instance =LeaveRequest.objects.get(id=request.POST['id'])
            form=LeaveAcceptForm(request.POST,instance=instance)
            mentor = form.save(commit=False)
            mentor.save()
            msg="Record saved"
        except:
            msg="Unable to process, Please check all values are present"
        return HttpResponse(json.dumps(dict(result=msg)), content_type="application/json")

###########################################ODView###########################################

class OdAddView(View):
	template_name='Od_admin_add.html'
	def get(self, request, *args, **kwargs):
	    form=OdForm
	    return render(request, self.template_name,{'form':form})
	def post(self, request, *args, **kwargs):
            form=OdForm(request.POST)
            odlist = form.save(commit=True)
            return HttpResponseRedirect('/admin/Od/')


class OdEditViewAjax(View):
        
        #On get it will fill table data
        def get(self, request, *args, **kwargs):
            odlist=OdList.objects.all()
            records=[]
            for record in odlist:
               records.append([record.id,record.purpose,record.date.strftime('%d/%m/%y'),record.staff.name,record.students])
            return HttpResponse(json.dumps(dict(data=records)), content_type="application/json")
             
        def post(self, request, *args, **kwargs):
            _od_id=request.POST['id']
	    if True:
		OdList.objects.filter(id=_od_id).delete()
                return HttpResponse("Record Deleted")
            else:
                return HttpResponse("Unable to delete record")

        
class OdEditView(View):
    template_name = 'od_edit.html'
    def get(self, request, *args, **kwargs):
        _od_id=args[0]
	odObj=OdList.objects.filter(id=_od_id)
        od=odObj.values()[0]
        od['id']=mentObj[0].id
       	od['staff']=mentObj[0].staff.id
	form=OdForm(od)
	print form
	return render(request,self.template_name,{'form':form})

    def post(self, request, *args, **kwargs):
        try:
            instance = OdList.objects.get(id=request.POST['id'])
            form=OdForm(request.POST,instance=instance)
            odlist = form.save(commit=False)
            odlist.save()
            msg="Record saved"
        except:
            msg="Unable to process, Please check all values are present"
        return HttpResponse(json.dumps(dict(result=msg)), content_type="application/json")

    def post(self, request, *args, **kwargs):
        pass

