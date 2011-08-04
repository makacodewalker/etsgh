'''
Created on Aug 4, 2011

@author: kidfisch
'''
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect


def home(request):
    t = loader.get_template('siteWelcome.html')
    c = Context(dict())
    return HttpResponse(t.render(c))