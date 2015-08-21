from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    #url(r'^$', 'onelead.views.home', name='home'),
    url(r'^platform/', include('lead_platform.urls')),
    url(r'^admin/', include('lead_admin.urls')),
    url(r'^login/', include('lead_auth.urls')),
    url(r'^logout/', include('lead_auth.urls')),
    url(r'^timetable/', include('lead_timetable.urls')),
    
)
