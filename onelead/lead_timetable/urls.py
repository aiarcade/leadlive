from django.conf.urls import patterns, include, url
from lead_timetable.views import TimeTableView
from lead_timetable.views import TimeTableAjax
from lead_timetable.views import TimeTableBatchView

urlpatterns = patterns('',
    (r'^open/(\d+)/$',TimeTableView.as_view()),
    (r'^ajax/$',TimeTableAjax.as_view()),
    (r'^batch/$',TimeTableBatchView.as_view()),
    
)
