from overviewer.utilities.template import Library
from django.core.urlresolvers import reverse, NoReverseMatch

register = Library()


def edit_url(model):
    label, name = model._meta.app_label, model.__class__.__name__.lower()
    try:
        return reverse('admin_%s_%s_change' % (label, name), args=(model.id,))
    except NoReverseMatch:
        return edit_url(model.parent)

register.filter(edit_url)


@register.filter
def add_url(model):
    label, name = model._meta.app_label, model._meta.object_name.lower()
    return reverse('admin_%s_%s_add' % (label, name))


@register.filter
def depth(object):
    return len(object.parents())


@register.filter
def should_open_in(object, current):
    if object == current:
        return True
    return object in current.parents() or current in object.parents()


@register.filter
def entries(objects, user):
    return objects.entries.manager(user.is_staff)


@register.setter
def group_by_day(list):
    day_dict = {}
    for object in list:
        day_dict.setdefault(object.published.day, []).append(object)
    return sorted(day_dict.items(), reverse=True)
