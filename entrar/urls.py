from django.conf.urls.defaults import *
from django.contrib import admin
admin.autodiscover()

from local_urls import urlpatterns

urlpatterns += patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^$', 'django.views.generic.simple.redirect_to', {'url': '/welcome/'}),
    (r'^(?P<slug>[-\w]+)/$', 'entries.views.entry'),
)
