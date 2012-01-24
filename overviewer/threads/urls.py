from django.conf.urls.defaults import patterns, url
from views import sections
from itertools import chain

def section(section):
    return (
        (r'^archives/%s/$' % section, section.archives),
        (r'^archives/%s/(?P<year>\d{4})/(?P<month>\d{1,2})/$' % section, section.archives),
        (r'^listing/%s/$' % section, section.listing),
        (r'^listing/%s/(?P<page>(\d+|last))/$' % section, section.listing),
        (r'^%s/$' % section, section.thread),
        (r'^%s/(?P<slug>[-\w]+)/$' % section, section.thread),
        (r'^%s/(?P<slug>[-\w]+)/(?P<ids>(\d+/)*)$' % section, section.entry),
    )

urlpatterns = patterns('', *chain(*map(section, sections)));
