from functools import update_wrapper
from datetime import timedelta
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from personal.utilities import truncate as trunc

register = template.Library()

def safefilter(fn):
    fn.is_safe = True
    return fn


@safefilter
@register.filter
@stringfilter
def style(string, dir=''):
    return '<link rel="stylesheet" type="text/css" href="/media/css/%s%s.css" />' % (dir, string)


@safefilter
@register.filter
@stringfilter
def script(string, dir=''):
    return '<script type="text/javascript" src="/media/js/%s%s.js"></script>' % (dir, string)


@register.filter
def datetime(datetime, string='%B %d, %Y at %H:%m'):
    return datetime.strftime(str(string))


@register.filter
def name(model):
    return model._meta.verbose_name.title()


@register.filter
def name_plural(model):
    return model._meta.verbose_name_plural.title()


@register.filter
def apply(fn, arg):
    return fn(arg)


@register.filter
def qualify(object, name=None):
    name = name or object.__class__.__name__.lower()
    return '?%s=%s' % (name, object.slug)


@register.filter
def truncate(object, length):
    return trunc(unicode(object), length)

@register.filter
def single(object):
    return object._meta.verbose_name

@register.filter
def plural(object):
    return object._meta.verbose_name_plural


@register.filter
def same_time(dtl, dtr):
    return abs(dtl - dtr) < timedelta(0, 60)


@register.filter
@stringfilter
def markdown(str):
    from pygment_markdown import pretty
    return mark_safe(pretty(str))
