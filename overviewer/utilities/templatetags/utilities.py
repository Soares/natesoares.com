from functools import partial, update_wrapper
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from overviewer.utilities.functional import curry
from overviewer.utilities.template import Library
from display import script, style, feeds
from memory import do_record, do_recall
import os

register = Library()

# Helpers

def safe(fn):
    fn.is_safe = True
    return fn


def texttag(fn):
    return safe(register.simple_tag(fn))


# Display utilities

texttag(script)
texttag(style)
texttag(feeds)



# Memory utilities

register.tag('record', do_record)
register.tag('recall', do_recall)



# Date utilities

@register.filter
def date(date, string='%B %d, %Y'):
    return date.strftime(str(string))


@register.filter
def datetime(datetime, string='%B %d, %Y at %H:%m'):
    return datetime.strftime(str(string))


@register.filter
def same_day(d1, d2):
    from datetime import datetime
    if isinstance(d1, datetime):
        d1 = d1.date()
    if isinstance(d2, datetime):
        d2 = d2.date()
    return d1 == d2



# Basic utilities


def qualify(list, name):
    return '&'.join('%s=%s' % (name, e) for e in list)
register.filter(qualify)


@register.filter
def xqualify(list, name):
    q = qualify(list, name)
    return (q + '&') if list else q


@register.filter
def rqualify(list, name):
    q = qualify(list, name)
    return ('?' + q) if list else q


@register.filter
def equals(a, b):
    return a == b


@register.filter
def single(object):
    return object._meta.verbose_name


@register.filter
def plural(object):
    return object._meta.verbose_name_plural


@register.filter
def is_in(elem, list):
    return elem in list if list else False


@register.filter
@stringfilter
def markdown(str):
    from pygment_markdown import pretty
    return mark_safe(pretty(str))


@register.filter
def chance(number):
    import random
    return random.randrange(number)


@register.simple_tag
def random_image(path):
    """
    Snipit taken and modified from http://www.djangosnippets.org/snippets/150/.
    Credit goes to pbx. Same with the is_image function below.
    """
    import posixpath, random,  settings
    ospath = os.path.join(settings.MEDIA_ROOT, path)
    pick = random.choice(filter(is_image, os.listdir(ospath)))
    return posixpath.join(settings.MEDIA_URL, path, pick)


def is_image(filename):
    ext = os.path.splitext(filename)[1]
    return ext in ('.jpg', '.jpeg', '.png', '.gif')
