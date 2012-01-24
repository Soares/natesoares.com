from datetime import date
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic.date_based import archive_month
from django.views.generic.list_detail import object_detail
from django.core.urlresolvers import reverse

from personal.tags.decorators import gets_tags
from personal.writing.models import Entry
from personal.projects.models import Project
from personal.activities.models import Activity
from personal.jobs.models import Job

start = date(2009, 4, 1)

@gets_tags
def entry(request, slug, tags):
    if request.user.is_staff:
        entries = Entry.all_objects.tagged_with(tags)
    else:
        entries = Entry.objects.tagged_with(tags)
    qualifiers = ['tags=%s' % (','.join(tags))] if tags else []
    def subset(model, field):
        name = model.__name__.lower()
        slug = request.GET[name]
        qualifiers.append('='.join((name, slug)))
        object = model.objects.get(slug=slug)
        return entries.filter(**{field: object}), object
    if 'project' in request.GET:
        entries, parent = subset(Project, 'projects')
    elif 'activity' in request.GET:
        entries, parent = subset(Activity, 'activities')
    elif 'job' in request.GET:
        entries, parent = subset(Job, 'jobs')
    else:
        parent = None
    qualifier = ('?' + '&'.join(qualifiers)) if qualifiers else ''
    try:
        nearby = dict(zip(('first', 'previous', 'next', 'latest'), entries.nearby(slug=slug)))
    except Entry.DoesNotExist, e:
        raise Http404(e)
    extra = dict(nearby, parent=parent, tags=tags, qualifier=qualifier)
    return object_detail(request, entries, slug=slug, extra_context=extra)


@gets_tags
def archives(request, tags, year=None, month=None):
    current_month = date.today().replace(day=1)
    month = str(current_month.month) if month is None else month
    year = str(current_month.year) if year is None else year
    then = date(int(year), int(month), 1)

    extra = dict(model=Entry, tags=tags,
				 qualifier='?tags=%s' % ','.join(tags) if tags else '',
                 first_month=date(start.year, start.month, 1),
                 latest_month=current_month if then < current_month else None)

    # I'm so witty.
    back = months_back(then)
    if back is 27:
        raise Http404("Ok, fine. Here's a 404. Happy?")
    if back in conversation:
        extra['message'] = conversation[back]
    if back > 52:
        return redirect('http://www.google.com/search?q=Something%20more%20interesting')

    if request.user.is_staff:
        entries = Entry.all_objects.tagged_with(tags)
    else:
        entries = Entry.objects.tagged_with(tags)
    return archive_month(request, year, month, entries, 'created',
        template_name='writing/archives.html',
        allow_empty=True,
        month_format='%m',
        extra_context=extra)


def months_back(then):
    return ((start.year - then.year) * 12) + (start.month - then.month)


conversation = {
    3: "This is before I even started the website. There's nothing here.",
    8: "Seriously. Stop it. There's nothing here. I hadn't even made the website yet.",
    12: "Stop following me!",
    13: "I mean it.",
    16: "What, do you think there are secrets ahead or something?",
    24: "There aren't. These pages are auto generated.",
    25: "Auto generated, you hear? They go on *forever*.",
    26: "FOREVER. That's how long these pages go on.",
    28: "Oooooh, you can edit a url. So what.",
    30: "Fine. Keep going back. See if I care.",
    31: "Whatever. I don't even like you anyway.",
    42: "Alright! You got here. Cool. Good job.",
    43: "You can leave now.",
    51: "Alright, fine, you win. I concede.",
    52: "If you're so damn bored, I'll redirect you somewhere more interesting.",
}
