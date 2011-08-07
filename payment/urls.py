from django.conf.urls.defaults import *

urlpatterns = patterns('',
#url(r'^$', 'payment.views.paymentHome'),
url(r'^viewcart$', 'payment.views.Cart_view'),
)
