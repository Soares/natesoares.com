from overviewer.utilities.template import Library
from overviewer.threads.models import Project

register = Library()

@register.filter
def description(phase):
    return Project.phase_descriptions[Project.phase_map[phase]]
