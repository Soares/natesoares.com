from datetime import date
from functools import partial
from django.shortcuts import get_object_or_404, redirect
from overviewer.utilities.views import render_to_404
from overviewer.comments.views import render
from overviewer.utilities.dateutils import month_diff
from django.views.generic.date_based import archive_month
from django.views.generic.list_detail import object_list
from itertools import chain
import models

start_date = date(2009, 4, 1)


class Section(object):
    num_per_page = 20

    conversation = {
        3: "This is before I even started the website. There's nothing here.",
        8: "Seriously. Stop it. There's nothing here. I hadn't even made the website yet.",
        12: "Stop following me!",
        13: "I mean it.",
        16: "What, do you think there are secrets ahead or something?",
        17: "There aren't any secrets.",
        18: "Why would there be secrets?",
        24: "Seriously. No secrets. These pages are auto generated.",
        25: "Auto generated, you hear? They go on *forever*.",
        26: "FOREVER. That's how long these pages go on.",
        28: "Oooooh, you can edit a url. So what.",
        29: "There's still nothing here.",
        31: "Fine. Keep going back. See if I care.",
        33: "Whatever. I don't even like you anyway.",
        42: "Ok, that's it. You win! You made it. Cool. Good job.",
        43: "Congratulations.",
        44: "Huzzah.",
        45: "Here comes your prize...",
        47: "You really should have seen that coming.",
        49: "Alright, that's it.",
        50: "You can leave now.",
        56: "Wow, you're a tenacious one.",
        62: "Alright, I concede.",
        63: "If you're so damn bored, I'll redirect you somewhere more interesting.",
    }

    def __init__(self, model, default='listing', private=False):
        self.model = model
        self.entry_model = model.entry_model()
        self.private = private
        self.default = getattr(self, default)

    def all_relevant(self, unpublished=False, limit=None):
        models = self.model.manager(unpublished).order_by('-published').all()
        entries = self.entry_model.manager(unpublished).order_by('-published').all()
        if limit is not None:
            models = models[:limit]
            entries = entries[:limit]
        return chain(models, entries)

    def recent_updates(self, count=4):
        sorter = lambda x, y: -cmp(x.published, y.published)
        return sorted(self.all_relevant(limit=count), sorter)[:count]

    def objects(self, request):
        return self.model.manager(request.user.is_staff).all()

    def get_entry(self, parent, num, is_staff):
        """ Get an entry ranked num off of parent """
        return get_object_or_404(parent.entries.manager(is_staff), rank=num)

    def administrate(self, request, entry):
        """ Do administrative tasks on the entry """
        if not request.user.is_staff:
            return
        if 'publish' in request.POST:
            entry.publish()
        if 'pull' in request.POST:
            entry.pull()
        if 'publish-all' in request.POST:
            entry.ancestor().publish_all()
        if 'disable_comments' in request.POST:
            entry.enable_comments = True
            entry.save()
        if 'enable_comments' in request.POST:
            entry.enable_comments = False
            entry.save()

    def processor(self, request):
        return {'section': self}

    def list_processor(self, request):
        return {'tags': request.GET.getlist('tag')}

    def listing_processor(self, request):
        return self.list_processor(request)

    def archive_processor(self, request):
        return dict(self.list_processor(request), **{
            'first_month': start_date, 'this_month': date.today(),
        })

    def thread_processor(self, thread, request):
        objects = self.objects(request)
        return {
            'object': thread,
            'first': thread.first(objects),
            'previous': thread.previous(objects),
            'next': thread.next(objects),
            'newest': thread.newest(objects),
        }

    def entry_processor(self, entry, request):
        return {
            'object': entry,
            'previous': entry.previous(request.user.is_staff),
            'next': entry.next(request.user.is_staff),
        }

    def filter(self, request, objects):
        """ Filter objects from the request """
        tags = request.GET.getlist('tag')
        return objects.tagged_with(tags) if tags else objects

    def goto(self, request, thread):
        if 'goto' not in request.GET:
            return None
        goto = request.GET['goto']
        objects = self.filter(request, self.objects(request))
        for direction in 'first', 'previous', 'next', 'newest':
            if goto == direction:
                return redirect(getattr(thread, direction)(objects) or thread)

    # Actual views

    def thread(self, request, slug=None):
        objects = self.objects(request)
        if slug is None:
            thread = get_object_or_404(objects.all()[:1])
        else:
            thread = get_object_or_404(objects, slug=slug)
        self.administrate(request, thread)
        next = self.goto(request, thread)
        return next or render(request, thread.template(), processors=(
            self.processor, partial(self.thread_processor, thread),
        ))

    def entry(self, request, slug, ids):
        ids = ids.rstrip('/').split('/')
        thread = get_object_or_404(self.objects(request), slug=slug)
        getter = partial(self.get_entry, is_staff=request.user.is_staff)
        entry = reduce(getter, ids, thread)
        self.administrate(request, entry)
        next = self.goto(request, thread)
        template = entry.ancestor().entry_template()
        return next or render(request, template, processors=(
            self.processor, partial(self.entry_processor, entry),
        ))

    def archives(self, request, year=None, month=None):
        objects = self.filter(request, self.objects(request))

        current_month = date.today()
        month = month or str(current_month.month)
        year = year or str(current_month.year)
        then = date(int(year), int(month), 1)

        # I'm so witty.
        extra = {}
        back = month_diff(start_date, then)
        if back is 27:
            return render_to_404(request, "Ok, fine. Here's a 404. Happy?")
        if back is 46:
            return redirect('http://www.youtube.com/watch?v=oHg5SJYRHA0')
        if back in self.conversation:
            extra['message'] = self.conversation[back]
        if back > 63:
            return redirect('http://www.google.com/search?q=somewhere%20more%20interesting')

        processors = (self.processor, self.archive_processor)
        return archive_month(request, year, month, objects, 'published',
                             allow_empty=True, month_format='%m',
                             template_name=self.model.archives_template(),
                             context_processors=processors, extra_context=extra)

    def listing(self, request, page=1):
        objects = self.filter(request, self.objects(request))
        processors = (self.processor, self.listing_processor)
        return object_list(request, objects, self.num_per_page,
                           template_name=self.model.listing_template(),
                           context_processors=processors)

    def __str__(self):
        return self.model.root()


class ProjectSection(Section):

    def __init__(self, default='listing'):
        return super(ProjectSection, self).__init__(models.Project, default)

    def list_processor(self, request):
        base = super(ProjectSection, self).list_processor(request)
        phases = request.GET.getlist('phase')
        return dict(base, phases=phases)

    def filter(self, request, objects):
        objects = super(ProjectSection, self).filter(request, objects)
        phases = request.GET.getlist('phase')
        if not phases:
            return objects
        map = models.Project.phase_map
        return objects.filter(phase__in=(map[p] for p in phases))


jobs = Section(models.Job, private=True)
writing = Section(models.Writing, 'archives')
projects = ProjectSection()
tutorials = Section(models.Tutorial)
activities = Section(models.Activity, private=True)
sections = (writing, projects, tutorials, activities, jobs)
section_map = dict((str(s), s) for s in sections)


def new(request):
    top_entries = chain(*(s.all_relevant(limit=1) for s in sections))
    sorter = lambda x, y: -cmp(x.published, y.published)
    try:
        return redirect(sorted(top_entries, sorter)[0])
    except IndexError:
        return redirect('/about/')


def thread_processor(request):
    return {'sections': sections}
