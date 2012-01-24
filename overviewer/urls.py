from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout
from overviewer.meta.views import register
from overviewer.threads.views import new
from overviewer.threads.views import sections
from overviewer.threads.sitemaps import sitemaps
from overviewer.threads.feeds import feeds

admin.autodiscover()


urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/nate/webapps/overviewer/media'}),

    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    (r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': sitemaps}),
    (r'^(?P<section>.+)/sitemap\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),

    (r'^login/$', login),
    (r'^logout/$', logout, {'redirect_field_name': 'next'}),
    (r'^register/$', register),
    (r'^comments/', include('overviewer.comments.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^$', new),
    (r'^', include('overviewer.threads.urls')),
)
