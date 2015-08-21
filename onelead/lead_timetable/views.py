from django.shortcuts import render
from django.views.generic import View
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

import datetime
import time
from datetime import date


from lead_platform.models import  TimeTable
from lead_platform.models import  SubjectMap
from lead_platform.models import  BatchDivision


from lead_admin.views import LoginRequiredMixin,GroupRequiredMixin


DAY_SE_LABEL='DAY SESSION'
EVE_SE_LABEL='EVENING SESSION'
DAY_SE_SLOT=0
EVE_SE_SLOT=5


class TimeTableBatchView( LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'timetable_batch.html'
    
    def get(self, request, *args, **kwargs):
        _divs=BatchDivision.objects.filter(batch__status='Live')
        return render(request, self.template_name,{'divs':_divs})

    def post(self, request, *args, **kwargs):
        pass


class TimeTableView( LoginRequiredMixin,GroupRequiredMixin,View):
    template_name = 'timetable.html'
    
    def get(self, request, *args, **kwargs):
        _maps=SubjectMap.objects.filter(batch_div__id=int(args[0]))
        if(len(_maps)==0):
            return HttpResponse("No subjects allocated, Please add alocations first")
        _div_name=_maps[0].batch_div.getName()
        maps=[]
        for _map in _maps:
            maps.append(_map.tmapName())
        
        return render(request, self.template_name,{'maps':maps,'divid':args[0],'divname': _div_name})

    def post(self, request, *args, **kwargs):
        pass





class TimeTableAjax( LoginRequiredMixin,GroupRequiredMixin,View):
    
    def get(self, request, *args, **kwargs):
        div_id=int(request.GET['divid'])
        t_objs = TimeTable.objects.filter(sub_map__batch_div=div_id)
        data=[]
        for t_obj in t_objs:
            data.append({'id':t_obj.sid,'text':t_obj.sub_map.tmapName(),'start_date':
                t_obj.start_date_time.strftime('%d-%m-%Y %H:%M'),'end_date':t_obj.end_date_time.strftime('%d-%m-%Y %H:%M')})
        return HttpResponse(json.dumps(data), content_type="application/json")
        
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(TimeTableAjax, self).dispatch(*args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        data=[]
        print request.POST
        for _id in request.POST['ids'].split(','):
            if request.POST[str(_id)+'_!nativeeditor_status']=='inserted':
                t_obj=TimeTable()
                t_obj.start_date_time=datetime.datetime.strptime(request.POST[_id+'_start_date'],"%d/%m/%Y %H:%M")
                t_obj.end_date_time=datetime.datetime.strptime(request.POST[_id+'_end_date'],"%d/%m/%Y %H:%M")
                t_obj.sid=_id;
                sub_map_id=int(request.POST[_id+'_text'].split('/')[0])
                t_obj.sub_map=SubjectMap.objects.filter(id=sub_map_id)[0]
                t_obj.save()
                x=[{'status':'ok','tid':'','type':'inserted','sid':''}]
            if request.POST[str(_id)+'_!nativeeditor_status']=='updated':
                t_obj=TimeTable.objects.filter(sid=_id)[0]
                t_obj.start_date_time=datetime.datetime.strptime(request.POST[_id+'_start_date'],"%d/%m/%Y %H:%M")
                t_obj.end_date_time=datetime.datetime.strptime(request.POST[_id+'_end_date'],"%d/%m/%Y %H:%M")
                t_obj.sid=_id;
                sub_map_id=int(request.POST[_id+'_text'].split('/')[0])
                t_obj.sub_map=SubjectMap.objects.filter(id=sub_map_id)[0]
                t_obj.save()
                x=[{'status':'ok','tid':'','type':'updated','sid':''}]
            if request.POST[str(_id)+'_!nativeeditor_status']=='deleted':
                t_obj=TimeTable.objects.filter(sid=_id)[0].delete()
                x=[{'status':'ok','tid':'','type':'deleted','sid':''}]
        x=[{'status':'ok','tid':'','type':'updated','sid':''}]
        return HttpResponse(json.dumps(x), content_type="application/json")
            

            
        
        
    
    
    
    
