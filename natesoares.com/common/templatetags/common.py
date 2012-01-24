from datetime import datetime
from django import template

register = template.Library()


@register.filter
def visible_writing(object):
	return object.writing.filter(published__lte=datetime.now())


@register.filter
def has_visible_writing(object):
	return object.writing.filter(published__lte=datetime.now())[:1].count()
