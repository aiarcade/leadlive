from django.conf.urls import patterns, include, url
from django.contrib import admin
from lead_platform.views import InstructorDashBoardView
from lead_platform.views import  InstructorAttendanceView
from lead_platform.views import InstructorAttendanceDeleteAjax
from lead_platform.views import TimeTableAjax
urlpatterns = patterns('',

    url(r'^$', InstructorDashBoardView.as_view()),
    url(r'^attendance/(\d+)/(\d{4})/(\d+)/(\d+)/(\d+)/$',InstructorAttendanceView.as_view()),
    url(r'^pullrecords/$',InstructorAttendanceDeleteAjax.as_view()),
    url(r'^ajax/$',TimeTableAjax.as_view()),
    
)
