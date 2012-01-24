from django import template

register = template.Library()

@register.filter
def phase(phase):
    from personal.projects.models import phases
    phases = dict(phases)
    return phases[phase]
