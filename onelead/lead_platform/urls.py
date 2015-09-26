from django.conf.urls import patterns, include, url
from django.contrib import admin
from lead_platform.views import  InstructorDashBoardView
from lead_platform.views import  InstructorAttendanceView
from lead_platform.views import  InstructorAttendanceDeleteAjax
from lead_platform.views import  InstructorViewLeaveRequest
from lead_platform.views import  InstructorConfirmLeaveView
from lead_platform.views import  InstructorConfirmLeaveEditView


from lead_platform.views import  LeaveEditView
urlpatterns = patterns('',

    url(r'^$',InstructorDashBoardView.as_view()),
    url(r'^attendance/(\d+)/(\d{4})/(\d+)/(\d+)/(\d+)/$',InstructorAttendanceView.as_view()),
    url(r'^pullrecords/$',InstructorAttendanceDeleteAjax.as_view()),
    url(r'^leave/$',InstructorViewLeaveRequest.as_view()),
    url(r'^leave/confirm/$',InstructorConfirmLeaveView.as_view()),
    url(r'^leave/confirm/done/$',InstructorConfirmLeaveEditView.as_view()),		
    url(r'^leave/confirm/done/edit/$',LeaveEditView.as_view()),	
	
    
)
