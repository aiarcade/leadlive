from django.shortcuts import render
from django.views.generic import View
from datetime import date
from lead_platform.models import  BatchDivision
import json
from django.http import HttpResponse
import datetime
from lead_platform.models import  TimeTable
from lead_platform.models import  SubjectMap
import time

DAY_SE_LABEL='DAY SESSION'
EVE_SE_LABEL='EVENING SESSION'
DAY_SE_SLOT=0
EVE_SE_SLOT=5

 
# Create your views here.
class TimeTableView(View):
    template_name = 'timetable.html'
    
    def get(self, request, *args, **kwargs):
        from_date=date(int(args[0]),int(args[1]),int(args[2]))
        to_date=date(int(args[3]),int(args[4]),int(args[5]))
        
        return render(request, self.template_name,{'from':from_date.strftime('%Y-%m-%d'),'to':to_date.strftime('%Y-%m-%d')})

    def post(self, request, *args, **kwargs):
        pass

class TimeTableAjax(View):
    
    def get(self, request, *args, **kwargs):
        start = time.time()
        from_date=datetime.datetime.strptime(request.GET['from'], "%Y-%m-%d").date()
        to_date=datetime.datetime.strptime(request.GET['to'], "%Y-%m-%d").date()
        no_days= (to_date-from_date).days
        data={'h':{'0':{},'1':{'0':'ORDER','1':'DATE','2':'DAY'}},'data':{}}
        batch_divs=BatchDivision.objects.filter(batch__status='Live')
        count=3
        div_rows={}
        for div in batch_divs:
            data['h']['1'][str(count)]=div.getName()
            data['h']['0'][str(count)]=DAY_SE_LABEL
            div_rows[div.getName()]=[count]
            count=count+1
        for div in batch_divs:
            data['h']['1'][str(count)]=div.getName()
            data['h']['0'][str(count)]=EVE_SE_LABEL
            div_rows[div.getName()]=div_rows[div.getName()]+[count]
            count=count+1
        exist_timetable=TimeTable.objects.filter(date__range=[from_date.strftime('%Y-%m-%d'),to_date.strftime('%Y-%m-%d') ])
        r_count=2
        c_count=3
        for delta in range(no_days):
            data['data'][str(r_count)]={}
            c_count=3
            for div in batch_divs:
                data['data'][str(r_count)][str(c_count)]={'v':'','o':self.getSubjectMaps(div)}
                c_count=c_count+1
            r_count=r_count+1
        r_count=2
        d_ccount=c_count
        
        for delta in range(no_days):
            c_count=d_ccount
            for div in batch_divs:
                data['data'][str(r_count)][str(c_count)]={'v':'','o':self.getSubjectMaps(div)}
                c_count=c_count+1
            r_count=r_count+1
        
        for tt in  exist_timetable:
            _map=tt.sub_map.subject.short_name+'/'+tt.sub_map.staff.shotName()+'('+str(tt.sub_map.id)+')'
            row=(tt.date-from_date).days+2 #add no of header rows
            if tt.slot_no==str(EVE_SE_SLOT):
                col=div_rows[tt.sub_map.batch_div.getName()][1]
            else:
                col=div_rows[tt.sub_map.batch_div.getName()][0]
            
            data['data'][str(row)][str(col)]['v']= _map   
        end = time.time()
        print "consumed time",end-start    
        return HttpResponse(json.dumps(data), content_type="application/json")
    
    def getPos(date_from,q_date,slot_no,div_name):
        row=(q_date-date_from).days+1
        
    
    def getSubjectMaps(self,div):
        maps=SubjectMap.objects.filter(batch_div=div,status='Live')
        if len(maps)>0:
            r_maps=''
            for _map in maps:
                r_maps=r_maps+'#'+_map.subject.short_name+'/'+_map.staff.shotName()+'('+str(_map.id)+')'    
        else:
            r_maps='None'
        return r_maps
    def daterange(self,start_date, end_date):
        for n in range(int ((end_date - start_date).days)):
            yield start_date + datetime.timedelta(n)

    #TODO handle errors , message on merge across batches
    def post(self, request, *args, **kwargs):
        table=json.loads(request.body)['data']
        for r in range(len(table)):
            if r==0 or r==1:
                continue 
            for c in range(len(table[0])):
                if table[r][c]=='NA' or c==0 or c==1 or c==2 or table[r][c] is None:
                    continue
                
                _rdate=datetime.datetime.strptime(table[r][1],"%d/%m/%y").date()
                _map_id=int(table[r][c].split('(')[1].replace(')',''))
                _smap=SubjectMap.objects.filter(id=_map_id)[0]
                if table[0][c].find(EVE_SE_LABEL)>-1:
                    slot=EVE_SE_SLOT #Evening combined
                else:
                    slot=DAY_SE_SLOT #Day combined
                exits_entry=TimeTable.objects.filter(date=_rdate,slot_no=slot,sub_map=_smap)
                
                #check for a record update
                case='new'
                if len(exits_entry)==0:
                    tt_entry=TimeTable()
                else:
                    tt_entry= exits_entry[0]
                    case='update'
                #print tt_entry,case,tt_entry.slot_no,tt_entry.sub_map.id,tt_entry.date
                tt_entry.date=_rdate
                tt_entry.sub_map=_smap
                tt_entry.slot_no=slot
               
                tt_entry.save()
        return HttpResponse('saved') 


