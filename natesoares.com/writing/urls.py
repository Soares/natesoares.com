from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('personal.writing.views',
    url(r'^$', 'archives', name='writing.bare-archives'),
    url(r'^(?P<year>\d{4})/(?P<month>\d\d?)/$', 'archives', name='writing.archives'),
    url(r'^(?P<slug>[-\w]+)/$', 'entry'),
)
