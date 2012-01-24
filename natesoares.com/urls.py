from django.conf.urls.defaults import *
from django.contrib import admin
from personal.meta import feeds
import settings
admin.autodiscover()

feeds = {
    'entries': feeds.LatestEntries,
    'updates': feeds.LatestUpdates,
    'changes': feeds.LatestChanges,
    'atom-entries': feeds.AtomLatestEntries,
    'atom-updates': feeds.AtomLatestUpdates,
    'atom-changes': feeds.AtomLatestChanges,
}

urlpatterns = patterns('django.views.generic.simple',
    (r'^welcome/$', 'direct_to_template', {'template': 'welcome.html'}),
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),
)

urlpatterns += patterns('',
    (r'^$', 'personal.meta.views.new'),
    (r'^updates/', 'personal.meta.views.updates'),
    (r'^changes/', 'personal.meta.views.changes'),
    (r'^comments/', include('django.contrib.comments.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
    
    (r'^writing/', include('personal.writing.urls')),
    (r'^projects/', include('personal.projects.urls')),
    (r'^activities/', include('personal.activities.urls')),
    (r'^jobs/', include('personal.jobs.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

    (r'^admin/', include(admin.site.urls)),
)
