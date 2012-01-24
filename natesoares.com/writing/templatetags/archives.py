from django import template
from django.core.urlresolvers import reverse

register = template.Library()

@register.filter
def link(date, qualifier=''):
    kwargs = dict(year=str(date.year), month=str(date.month))
    return reverse('writing.archives', kwargs=kwargs) + qualifier
