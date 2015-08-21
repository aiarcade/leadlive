from django.conf.urls import patterns, include, url
from views import LoginView
from views import LogOutView


urlpatterns = patterns('',
    url(r'^$', LoginView.as_view()),
    url(r'^done/$', LogOutView.as_view()),
)
