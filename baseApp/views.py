# Create your views here.
from django.forms import ModelForm
from django.views.decorators.csrf import csrf_exempt
from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from models import *
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django import forms
import time
import random
import datetime
import re
from django.forms.widgets import *
from django.forms.extras.widgets import *
    
class AddForm(forms.Form):
    pass
#    
#class CartForm(ModelForm):
#    class Meta:
#        model =Cart
#

class TicketTypeForm(ModelForm):
    class Meta:
        model =TicketType
        exclude = ['cart'] 

class TicketForm(ModelForm):
    class Meta:
        model =Ticket 

class PayInForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']
           
class AddEventForm(ModelForm):
    class Meta:
        model=Event
        exclude=['created','event_Rep']
        
        
# Used to process Categories
CATEGORY_DICT = {}
for cat in CATEGORY_CHOICES:
    CATEGORY_DICT[cat[0]]=cat[1]
################################

def ticketHome(request):
    t = loader.get_template('baseApp_welcome.html')
    c = Context(dict())
    return HttpResponse(t.render(c))
    
def categories_list(request):
    category_list=CATEGORY_DICT.values()
    return render_to_response('baseApp_categoryView.html', {'category_list':category_list})

def events_list(request,categoryValue):
    event_list=[]
    for category in CATEGORY_DICT:
        if CATEGORY_DICT.get(category)==categoryValue:
            event_list = Event.objects.filter(category=category)
    return render_to_response('baseApp_eventList.html', {'events':event_list})

#def names_list(request):
#    name_list = Event.objects.all()
#    return render_to_response('baseApp_nameView.html', {'name_list':name_list})

#def venues_list(request):
#    venue_list = Event.objects.filter()
#    return render_to_response('baseApp_venueView.html', {'venue_list':venue_list})


def view_map(request,id):
    event = Event.objects.get(id=id)
    ticketsType=TicketType.objects.filter(event__id=id)
    return render_to_response('baseApp_map.html', {'event_details':event})

#def cart_list(request,id):
#    if id:        
#        cart = Ticket.objects.filter(Cart__id=id)
#        return render_to_response('baseApp_cart.html', {'cart':cart})
#    else:
#        return HttpResponse('<div align="center"><h5>Cart is empty</h5></div>')

def isPhone(inp):
    result = re.search(r'^[0][2|5][0|4|3|6|7|8]([0-9]){7}$', inp,re.L)
    # print result.groups() 
    if result:
        return True
    else:
        return False
     
@csrf_exempt
def event_detail(request,id):
    event = Event.objects.get(id=id)
    ticketsType=TicketType.objects.filter(event__id=id)
    allTickets = Ticket.objects.filter(event__id=id)
    tdate=str(datetime.datetime.today())
    tstr={}
    sum=0
    msg=''
    
    if request.method == 'POST':  
        form = AddForm()
        i=0
        if isPhone(request.POST['phone']):
             
            for i in range(len(ticketsType)):
                if request.POST.get(ticketsType[i].name, None):             
                    tstr[i]=ticketsType[i].name
                    
                    sum+=float(ticketsType[i].price)
                else:
                    pass
              
            #check if a ticket has been selected    
            if len(tstr)<1:
                msg="Please select a ticket"
                return render_to_response('baseApp_eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})                 
                   
            try:#Check for the availability of tickets
                
                for j in range(len(tstr)):
                    tyt=TicketType.objects.get(name=tstr[j])
                    tickets = Ticket.objects.filter(event=event,ticketType=tyt,paid=False)
                    if len(tickets)<1:
                        msg="sorry we have run out of "+tstr[j]+" tickets for this event"
                        return render_to_response('baseApp_eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})                
            except:
                msg="sorry we have run out of tickets for this event"
                return render_to_response('baseApp_eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})                 
                
            try:#checks the availability of cart thus if it already exists
                carte=Cart.objects.filter(cPhone=request.POST['phone'],paid=False)
                
                #if a cart is not available for the user(phone number) creates a cart 
                avail=len(carte)
                if avail==0:
                    c=Cart(cPhone=request.POST['phone'],value=str(sum),created=tdate)
                    c.save()
                       
                    try:# add tickets to cart      
                        cart=Cart.objects.get(cPhone=request.POST['phone'],paid=False)
                        for k in range(len(tstr)):  
                            
                            tyt=TicketType.objects.get(name=tstr[k]) 
                                     
                            tick = Ticket.objects.filter(event=event,ticketType=tyt,paid=False)[:1]
                            t = Ticket.objects.get(serialNo=tick[0])
    #                        return HttpResponse(t.paid) 
                            t.paid=True
                            t.cart=cart.cPhone                    
                            t.save()
                            msg='Ticket has been added to cart successfully. Click on cart to checkout or add more to cart'  
                            return render_to_response('baseApp_eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})     
                                
                    except:
                        msg='Tickets cannot be added, try again'
                        return render_to_response('baseApp_eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})                 
                    
                    
                if len(carte)>1 or len(carte)<0:
                    msg="A cart exists that you have not paid for"
                    return render_to_response('baseApp_eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg}) 
            
                #add tickets to cart if cart already exists     
                try:
                    cart=Cart.objects.get(cPhone=request.POST['phone'],paid=False)
                    for k in range(len(tstr)):  
                        
                        tyt=TicketType.objects.get(name=tstr[k]) 
                                 
                        tick = Ticket.objects.filter(event=event,ticketType=tyt,paid=False)[:1]
                        t = Ticket.objects.get(serialNo=tick[0])
#                        return HttpResponse(t.paid) 
                        t.paid=True
                        t.cart=cart.cPhone                    
                        t.save()
                        msg='Ticket has been added to cart successfully. Click on cart to checkout or add more to cart'  
                        return render_to_response('baseApp_eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})     
                                    
                except:
                    msg='failed to add Ticket, try again1'
                    return render_to_response('baseApp_eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg}) 
                        
                
            except:
                return HttpResponse('error') 
            
        else:
            msg='Please enter a valid phone number'
            return render_to_response('baseApp_eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets,'msg':msg})        
          
    else:
        form = AddForm()
        return render_to_response('baseApp_eventDetails.html', {'event_details':event,'form':form.as_p(),'ticket_types':ticketsType,'tickets':allTickets})
    
@csrf_exempt
def addEvent_view(request):
    #if request.user.is_authenticated():
    try:    # Try to get existing profile
        userInfo = UserProfile.objects.get(user=request.user)        
    except: # create profile for user
        userInfo = UserProfile(user=request.user)
        
    if request.method == 'POST':                   
        payForm = PayInForm(request.POST, instance = userInfo)
        if payForm.is_valid():
            payForm.save()
            msg="Pay In Account successfully saved"
            eventForm = AddEventForm()
            return render_to_response('baseApp_addEvent.html', {'user':userInfo,'payForm':payForm.as_p(),'eventForm':eventForm.as_p(),'logged_in':request.user.is_authenticated(),'msg':msg})
        
        event=Event(event_Rep=request.user,created=str(datetime.datetime.today()))
        try:    #try to create an event
            eventForm = AddEventForm(request.POST, instance=event)
            if eventForm.is_valid():
                eventForm.save()
                msg="Your event has been saved successfully"
                ticketTypeForm = TicketTypeForm()
                return render_to_response('baseApp_ticket.html', {'ticketTypeForm':ticketTypeForm.as_p(),'logged_in':request.user.is_authenticated(),'msg':msg})
            
            ticketType=TicketType(event=event)
            ticketTypeForm = TicketTypeForm(request.POST, instance = ticketType)
            if ticketTypeForm.is_valid():
                ticketTypeForm.save()
                tt = TicketType.objects.get(event=event)
                
            #generate tickets
                for i in range(int(request.POST['qty'])):
                    pin=int(random.random()*10000000000000)
                    s=int(random.random()*100000000)
                    sn="SN"+str(s)
                    t=Ticket(event=event,ticketType=tt,pin=pin,serialNo=sn)
                    t.save()
            
                msg=str(request.POST['qty'])+' '+str(tt.name)+" tickets have been generated for "+str(tt.event)
                return render_to_response('baseApp_ticket.html', {'ticketTypeForm':ticketTypeForm.as_p(),'logged_in':request.user.is_authenticated(),'msg':msg})
        
        
        except:
            eventForm = AddEventForm(request.POST, instance=event)
            msg="an event with this name already exists"
            return render_to_response('baseApp_addEvent.html', {'user':userInfo,'payForm':payForm.as_p(),'eventForm':eventForm.as_p(),'logged_in':request.user.is_authenticated(),'msg':msg})               
    
    else:
        payForm = PayInForm(instance=userInfo)
        event=Event(event_Rep=request.user,created=str(datetime.datetime.today()))
        eventForm = AddEventForm(instance=event)
        msg=''
        return render_to_response('baseApp_addEvent.html', {'user':userInfo,'payForm':payForm.as_p(),'eventForm':eventForm.as_p(),'logged_in':request.user.is_authenticated(),'msg':msg})
        
#    else:
#        userInfo =UserProfile()
#        payForm = PayInForm(instance=userInfo)
#        eventForm = AddEventForm()
#        msg=''
#        return render_to_response('baseApp_addEvent.html', {'user':userInfo,'payForm':payForm.as_p(),'eventForm':eventForm.as_p(),'logged_in':request.user.is_authenticated(),'msg':msg})


@csrf_exempt
def ticket_view(request): 
    return HttpResponse('cut') 

#@csrf_exempt
#def Cart_view(request):
#    if request.method == 'POST':
#        if request.POST.get("phone", None): 
#            cart=Cart.objects.filter(cPhone=request.POST['phone'],paid=False)
#            return render_to_response('baseApp_cartlist.html', {'cart':cart })
#    else:
#        form = CartForm()
        #end of form code
#        return render_to_response('baseApp_cart.html', {'form':form.as_p() })

