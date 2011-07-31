from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
#from django import oldforms as forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import *
from django.shortcuts import render_to_response, render
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm
from baseApp.models import *
from django.core import validators
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

#class ProfileForm(ModelForm):
#    class Meta:
#        model = UserProfile
    
@csrf_exempt
def signupView(request):
    form = UserCreationForm(data = request.POST)
    if (form.is_valid()):
        new_user = form.save()
        new_user = authenticate(username = form.cleaned_data['username'],password = form.cleaned_data['password1'])
        login(request, new_user)
        return render_to_response('reg/login.html', { 'form':form,'logged_in': request.user.is_authenticated() })
        
    #return render_to_response("reg/signup.html", {'form' : forms.FormWrapper(form, data, errors)} )
    return render_to_response("reg/signup.html", {'form' : form })
# Extras that didn't work out 'name_error_msg': 'Sorry, this username has already been taken.', 'passwd_error_msg':'Passwords do not match.'

@csrf_exempt
def loginView(request):
    """Logs a user into the application."""
    
    # Initialize the form either fresh or with the appropriate POST data as the instance
    auth_form = AuthenticationForm(None, request.POST or None)
    
    if request.user.is_authenticated():
        #return HttpResponseRedirect(reverse('reg:login'))
        return render_to_response('reg/login.html', { 'auth_form': auth_form,'title': 'User Login','logged_in': request.user.is_authenticated() })
        
    # Ye Olde next param so common in login.
    # I send them to their default profile view.
    #nextpage = request.GET.get('next', reverse('account:index'))
 
    # The form itself handles authentication and checking to make sure passowrd and such are supplied.
    if auth_form.is_valid():
        login(request, auth_form.get_user())
        #return HttpResponseRedirect(nextpage)
        return render_to_response('reg/login.html', { 'auth_form': auth_form,'title': 'User Login','logged_in': request.user.is_authenticated() })
    
    #return render(request, 'reg/login.html', {'auth_form': auth_form,'title': 'User Login','next': nextpage })
    return render_to_response('reg/login.html', { 'auth_form': auth_form,'title': 'User Login','logged_in': request.user.is_authenticated() })
   
   
@csrf_exempt
def logoutView(request):
    logout(request)
    return render_to_response('reg/logout.html')# Create your views here.