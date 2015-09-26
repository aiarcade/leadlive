from django.conf.urls import patterns, include, url
from django.contrib import admin
from lead_student.views import StudentDashBoardView

urlpatterns = patterns('',

    url(r'^$', StudentDashBoardView.as_view()),
    
    
)
