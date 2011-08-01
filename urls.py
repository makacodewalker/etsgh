from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ETS.views.home', name='home'),
    # url(r'^ETS/', include('ETS.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^baseApp/', include('baseApp.urls')),
    url(r'^baseApp/reg/', include('reg.urls')),
)	

#if settings.DEBUG:
#  urlpatterns += patterns('django.views.static',
#    (r'^%s(?P<path>.*)$' % (settings.MEDIA_URL[1:],), 'serve', {
#      'document_root': settings.MEDIA_ROOT,
#      'show_indexes': True }),)

#(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/path/to/media'}),
