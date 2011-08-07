from django.template import Context, loader
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from baseApp.models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.forms import ModelForm
from django.contrib.auth.models import User
import time
import re
# Create your views here.



class OutgoingSMSForm(ModelForm):
    class Meta:
        model = OutgoingSMS
        exclude = ['receiver','message','sent','created']
    
class CartForm(ModelForm):
    class Meta:
        model =Cart

def cart_list(request,id):
    if id:        
        cart = Ticket.objects.filter(Cart__id=id)
        return render_to_response('payment_cart.html', {'cart':cart})
    else:
        return HttpResponse('<div align="center"><h5>Cart is empty</h5></div>')

@csrf_exempt
def Cart_view(request):
    if request.method == 'POST':
        if request.POST.get("phone", None): 
            cart=Cart.objects.filter(cPhone=request.POST['phone'],paid=False)
            return render_to_response('payment_cartlist.html', {'cart':cart })
    else:
        form = CartForm()
        #end of form code
        return render_to_response('payment_cart.html', {'form':form.as_p() })


def processIncomingSMS(request):    # processes all sms received from mobile money providers
    time.sleep(10)
    smsleft = IncomingSMS.objects.filter(read = False)
    for sms in smsleft:
        result = re.search(r'(.*)transactionid:(.*)(\d+)\namount:(.*)(\d+)', sms.message)
        sms.transactionID = result.group(2)
        sms.amount = result.group(4)

        
def redeemCart(request, phoneNumber, transID='blank'): # Get cart thats unpaid for
    cartRecords = Cart.objects.filter(cPhone = phoneNumber)
    cart2redeem = cartRecords.objects.get(paid = False)
    if transID != 'blank' and IncomingSMS.objects.get(transactionID = transID):
        cart2redeem.paid = True
        ticketsBought=Ticket.objects.filter(cart__id = cart2redeem)
        phoneNumStr= 'These tickets have been sent to: '+str(phoneNumber)+'\n'
        ticketStr=''
        for ticket in ticketsBought:
            ticketStr = str(ticket.event)+str(ticket.pin)+str(ticket.ticketType)+'\n'
        smsBody = phoneNumStr+ticketStr
        content = OutgoingSMS(receiver=phoneNumber,message=smsBody,sent=False)
        form = OutgoingSMSForm(request.POST, instance = content)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    else:
        form = OutgoingSMSForm(instance = content)
