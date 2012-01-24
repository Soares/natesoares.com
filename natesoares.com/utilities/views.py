from itertools import chain
from personal.writing.models import Entry
from personal.projects.models import Project
from personal.activities.models import Activity
from personal.jobs.models import Job

def get_top(count, tags, ordering):
    if ordering[0] == '-':
        reversed, attr = True, ordering[1:]
    else:
        reversed, attr = False, ordering
    models = Entry, Project, Activity, Job
    objects = chain(*(m.objects.tagged_with(tags).order_by(ordering)[:count] for m in models))
    compare = lambda x, y: cmp(getattr(x, attr), getattr(y, attr))
    return sorted(objects, compare, reverse=reversed)[:count]


def top(count, tags=None):
    return get_top(count, tags, '-published')


def top_changes(count, tags=None):
    return get_top(count, tags, '-updated')
