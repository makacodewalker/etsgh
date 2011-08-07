from django.conf.urls.defaults import *

urlpatterns = patterns('',
#url(r'^$', 'reg.views.regHome'),
url(r'^login$', 'reg.views.loginView'),
url(r'^logout$', 'reg.views.logoutView'),
url(r'^signup$', 'reg.views.signupView'),
)

