from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('overviewer.comments.views',
    (r'^new/$', 'new'),
    (r'^edit/(?P<id>\d+)/$', 'edit'),
    (r'^remove/(?P<id>\d+)/$', 'remove'),
    (r'^form/(?P<id>\d+)/$', 'form'),
    (r'^continue/(?P<id>\d+)/$', 'continue_thread'),
)

urlpatterns += patterns('',
    (r'^', include('django.contrib.comments.urls')),
)
