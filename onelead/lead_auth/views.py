from django.shortcuts import render
from django.views.generic import View
from django.views.decorators.csrf  import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect

from django.contrib.auth import authenticate,login,logout
from lead_platform.models import Staff


class LoginView(View):
    template_name = 'login.html'

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name,{'msg':''})
        
        
    def post(self, request, *args, **kwargs):
        user=authenticate(username=request.POST['loginid'],password=request.POST['password'])
        if user is not None:
            group=user.groups.all()[0].name
            request.session['_id']=user.username
            login(request, user)
            if group=='students':
                return HttpResponseRedirect('/students/')
            elif group=='staff':
                return HttpResponseRedirect('/platform/')
            elif group=='administration' :
                return HttpResponseRedirect('/admin/')
        else:
            return render(request, self.template_name,{'msg':'Invald user name or password'})

class LogOutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/login/')
