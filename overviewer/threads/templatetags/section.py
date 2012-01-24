from overviewer.utilities.template import Library
from django.core.urlresolvers import reverse

register = Library()


@register.simple_tag
def archives(section, year=None, month=None):
    if year is not None:
        return reverse(section.archives, args=(year, month))
    return reverse(section.archives)


@register.simple_tag
def listing(section, page=1):
    return reverse(section.listing, args=[page])


@register.simple_tag
def section_default(section):
    return reverse(section.default)


@register.filter
def feed(section, object):
    if hasattr(object, 'parent'):
        return 'subentries/%s/%s' % (section, object.id)
    return 'entries/%s/%s' % (section, object.slug)


@register.filter
def feed_title(section, object):
    return 'Sub-entries in %s' % object
