from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'views.home', name='home'),
    url(r'^aboutus$', 'views.aboutUs'),
    url(r'^search$', 'views.search'),
    url(r'^help$', 'views.siteHelp'),
    url(r'^suggestions$', 'views.addSuggestion'),
    url(r'^editsuggestion_(?P<id>\d+)$', 'views.editSuggestion'),

	# reg urls, instead of include('reg.urls')
    url(r'^reg_login$', 'reg.views.loginView'),
    url(r'^reg_logout$', 'reg.views.logoutView'),
    url(r'^reg_signup$', 'reg.views.signupView'),

	# baseApp urls, instead of include('baseApp.urls')
	url(r'^baseApp$', 'baseApp.views.ticketHome'),
	url(r'^baseApp_bycategory$', 'baseApp.views.categories_list'),
	#url(r'^baseApp_byname$', 'baseApp.views.names_list'),
	#url(r'^baseApp_byvenue$', 'baseApp.views.venues_list'),
	url(r'^baseApp_events_(?P<categoryValue>((\/?\(?\w+\)?\/?\s?)+))$', 'baseApp.views.events_list'),
	url(r'^baseApp_(detail|info)_(?P<id>\d+)$', 'baseApp.views.event_detail'),
	url(r'^baseApp_map_(?P<id>\d+)$', 'baseApp.views.view_map'),
	url(r'^baseApp_addEvent$', 'baseApp.views.addEvent_view'),
	url(r'^baseApp_tickets$', 'baseApp.views.ticket_view'),
	
	# payment urls, instead of include('payment.urls')
	#url(r'^payment$', 'payment.views.paymentHome'),
	url(r'^payment_viewcart$', 'payment.views.Cart_view'),


    # url(r'^ETS/', include('ETS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^baseApp/', include('baseApp.urls')),
    #url(r'^payment/', include('payment.urls')),
    #url(r'^reg/', include('reg.urls')),
)	

#if settings.DEBUG:
#  urlpatterns += patterns('django.views.static',
#    (r'^%s(?P<path>.*)$' % (settings.MEDIA_URL[1:],), 'serve', {
#      'document_root': settings.MEDIA_ROOT,
#      'show_indexes': True }),)

#(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/path/to/media'}),
