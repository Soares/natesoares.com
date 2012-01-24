from utilities import template
from django.conf import settings
register = template.Library()


def taglist(tag, *files):
    def accumulate((total, directory), name):
        if name.endswith('/'):
            return total, name
        return total + (tag % (directory + name)), directory
    return reduce(accumulate, files, ('', ''))[0]


# Script and style

def style(*styles):
    return taglist('<link rel="stylesheet" type="text/css" href="{media}css/%s.css">'.format(media=settings.MEDIA_URL), *styles)

style.is_safe = True
register.simple_tag(style)


def script(*scripts):
    return taglist('<script type="text/javascript" src="{media}js/%s.js"></script>'.format(media=settings.MEDIA_URL), *scripts)

script.is_safe = True
register.simple_tag(script)


def atom(name, title):
    return '<link href="/feeds/%s/" rel="alternate" type="application/atom+xml" title="%s">' % (name, title)

atom.is_safe = True
register.simple_tag(atom)


def edit_url(model):
    from django.core.urlresolvers import reverse
    label, name = model._meta.app_label, model.__class__.__name__.lower()
    return reverse('admin_%s_%s_change' % (label, name), args=(model.pk,))

register.filter(edit_url)
