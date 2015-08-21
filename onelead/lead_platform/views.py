from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .models import SubjectMap
from .models import Student
from .models import Staff
from .models import Attendance
from .models import TimeTable
from datetime import date
import datetime
import json
from django.views.decorators.csrf  import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User

class InstructorDashBoardView(View):
    template_name = 'instructor_base.html'
    
    def get(self, request, *args, **kwargs):
        _id=1#request.session['_id']
        
        return render(request, self.template_name,{})

    def post(self, request, *args, **kwargs):
        pass


class TimeTableAjax(View):
    
    def get(self, request, *args, **kwargs):
        staff_id=int(request.GET['staffid'])
        t_objs = TimeTable.objects.filter(sub_map__staff__id=staff_id)
        data=[]
        for t_obj in t_objs:
            data.append({'id':t_obj.sid,'text':t_obj.sub_map.tmapName(),'start_date':
                t_obj.start_date_time.strftime('%d-%m-%Y %H:%M'),'end_date':t_obj.end_date_time.strftime('%d-%m-%Y %H:%M')})
        return HttpResponse(json.dumps(data), content_type="application/json")
        

class InstructorAttendanceView(View):
    template_name = 'attendance.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        _r_map=args[0]
        _slot=args[4]
        _date=date(int(args[1]),int(args[2]),int(args[3]))
        _sub_map=SubjectMap.objects.filter(id=_r_map)[0]
        students=Student.objects.filter(batch_div=_sub_map.batch_div)
        _attendance=[]
        empty_attendance=[]
        marked_on_theday =Attendance.objects.filter(date=_date,sub_map__batch_div=_sub_map.batch_div).values('slot_no','sub_map__subject__name','sub_map').distinct()
        print marked_on_theday
            
        for _student in students:
            attendance=Attendance.objects.filter(date=_date,sub_map=_sub_map,student=_student,slot_no=_slot)
            if len(attendance)>0:
                _attendance.append({'name':_student.name,'id':_student.admission_no,'status':attendance[0].status_of_student,'roll':_student.roll_no})
            else:
                empty_attendance.append({'name':_student.name,'id':_student.admission_no,'status':'P','roll':_student.roll_no})
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
        #print request.POST
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


class InstructorAttendanceDeleteAjax(View):
        
        
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
             
             
             
             
             
        
