'''
Created on Aug 4, 2011

@author: kidfisch
'''
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from baseApp.models import *
from django.forms import ModelForm
from django.shortcuts import render_to_response

def home(request):
    t = loader.get_template('siteWelcome.html')
    c = Context(dict())
    return HttpResponse(t.render(c))

def aboutUs(request):
    return render_to_response('aboutus.html')

def search(request):
    return render_to_response('search.html')

def siteHelp(request):
    return render_to_response('siteHelp.html')


class SuggestionForm(ModelForm):
    class Meta:
        model=Suggestion
        exclude = ['created',]

@csrf_exempt
def addSuggestion(request):
    suggestions = Suggestion.objects.all()
    msg=''
    #Start of form code
    comment = Suggestion()
    if request.method == 'POST':
        if request.user.is_authenticated():
            comment = Suggestion(author=request.user.username)
        else:
            comment = Suggestion()

        form = SuggestionForm(request.POST, instance = comment)
        if form.is_valid():
            form.save()
            msg = 'Thank You for your comment'
            return render_to_response('suggestions.html', {'suggestions':suggestions,'msg':msg,'form':form.as_p() })
    else:
        form = SuggestionForm()
        #end of form code
        return render_to_response('suggestions.html', {'suggestions':suggestions,'msg':msg,'form':form.as_p() })


@csrf_exempt
def editSuggestion(request, id):
    msg=''
    comment = Suggestion.objects.get(id=id)
    #Start of form code
    if request.user.username == comment.author:
        same = True
        if request.method == 'POST':
            form = SuggestionForm(request.POST, instance = comment)
            if form.is_valid():
                form.save()
                msg = 'Thank You for your comment'
                return render_to_response('editsuggestion.html', {'msg':msg,'form':form.as_p(),'logged_in':request.user.is_authenticated(),'same':same })    
        else:
            form = SuggestionForm(instance = comment)
            #end of form code
            return render_to_response('editsuggestion.html', {'msg':msg,'form':form.as_p(),'logged_in':request.user.is_authenticated(),'same':same })
    else:
        same = False
        msg = 'To edit this comment, you must be logged in and be its original author.'
        form = SuggestionForm()
        return render_to_response('editsuggestion.html', {'msg':msg,'form':form.as_p(),'logged_in':request.user.is_authenticated(), 'same':same })
        
