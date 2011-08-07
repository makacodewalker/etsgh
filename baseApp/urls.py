from django.conf.urls.defaults import *

urlpatterns = patterns('',
url(r'^$', 'baseApp.views.ticketHome'),
url(r'^bycategory$', 'baseApp.views.categories_list'),
#url(r'^byname$', 'baseApp.views.names_list'),
#url(r'^byvenue$', 'baseApp.views.venues_list'),
url(r'^events/(?P<categoryValue>((\/?\(?\w+\)?\/?\s?)+))$', 'baseApp.views.events_list'),
url(r'^(detail|info)/(?P<id>\d+)$', 'baseApp.views.event_detail'),
url(r'^map/(?P<id>\d+)$', 'baseApp.views.view_map'),
url(r'^addEvent$', 'baseApp.views.addEvent_view'),
url(r'^tickets$', 'baseApp.views.ticket_view'),
#url(r'^viewcart$', 'baseApp.views.Cart_view'),
)
