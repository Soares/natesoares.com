from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from itertools import chain

from django.db import models
from datetime import date, datetime
from tags.models import Taggable
from threads.managers import PublishableManager, VisibleManager
from threads.managers import SubEntryManager, VisibleSubEntryManager
from utilities.models import choices, Ordered



########################################################################
# Base models


class Entry(Ordered):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    published = models.DateTimeField(blank=True, null=True)
    enable_comments = models.BooleanField(default=True)

    objects = PublishableManager()
    visible = VisibleManager()

    @classmethod
    def manager(cls, unpublished=False):
        return cls.objects if unpublished else cls.visible

    class Meta:
        abstract = True
        ordering = '-published',

    def publish(self):
        if not self.published:
            now = datetime.now()
            self.save()

    def pull(self):
        if self.published:
            self.published = None
            self.save()

    def parents(self):
        if hasattr(self, 'parent'):
            return (self.parent,) + self.parent.parents()
        return ()

    def traverse(self):
        yield self
        if hasattr(self, 'entries'):
            for e in chain(*(e.traverse() for e in self.entries.all())):
                yield e


class Thread(Entry, Taggable):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=128)
    subtext = models.CharField(max_length=255, blank=True)

    class Meta(Entry.Meta):
        abstract = True

    @classmethod
    def section(cls):
        from views import section_map
        return section_map[cls.root()]

    @classmethod
    def entry_model(cls):
        try:
            return cls.entries.related.model
        except AttributeError:
            return cls.entries.field.rel.to

    @classmethod
    def root(cls):
        return cls._meta.verbose_name_plural.decode()

    @classmethod
    def single(cls):
        return cls._meta.verbose_name.decode()

    @classmethod
    def template(cls):
        return '%s/thread.html' % cls.root(), 'threads/thread.html'

    @classmethod
    def entry_template(cls):
        return '%s/entry.html' % cls.root(), 'threads/entry.html'

    @classmethod
    def archives_template(cls):
        return '%s/archives.html' % cls.root(), 'threads/archives.html'

    @classmethod
    def listing_template(cls):
        return '%s/listing.html' % cls.root(), 'threads/listing.html'

    def ancestor(self):
        """
        Threads can have entries attached, which can have entries attached,
        and so on. Threads are ancestors in such entry trees.
        """
        return self

    def follower(self, is_staff):
        """
        When an entry has no siblings ahead of it and wants to know what
        entry comes next in the tree traversal, it will ask its parent
        for the follower. Threads return themselves, so that if you are on
        the very last entry in an entry tree and you ask for the next entry,
        you'll get back to the top.
        """
        return self

    def publish_all(self):
        self.publish()
        for e in self.entries.all():
            e.publish_all()

    def get_absolute_url(self):
        return '/%s/%s/' % (self.root(), self.slug)

    def __unicode__(self):
        return self.name


class ThreadEntry(Entry, Ordered):
    rank = models.SmallIntegerField(blank=True)
    name = models.CharField(max_length=128)
    subtext = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    objects = SubEntryManager()
    visible = VisibleSubEntryManager()

    class Meta:
        abstract = True
        ordering = 'rank',
        unique_together = 'parent', 'rank'

    def save(self, *args, **kwargs):
        if self.rank is None:
            prev = self.parent.entries.order_by('-rank').first()
            self.rank = (prev.rank + 1) if prev else 0
        return super(ThreadEntry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return '%s%d/' % (self.parent.get_absolute_url(), self.rank)

    def ancestor(self):
        return self.parent.ancestor()

    def siblings(self, is_staff=False):
        relatives = self.manager(is_staff).exclude(id=self.id)
        return relatives.with_parent(self.parent)

    def follower(self, is_staff):
        """
        Either grab the next sibling in line or, if you have no 
        younger siblings, then grab your parent's follower.
        """
        next = self.after(self.siblings(is_staff)).first()
        return next or self.parent.follower(is_staff)

    def last_entry(self, is_staff=False):
        """
        The entry you get if you traverse all the way down this
        node in the entry tree.
        """
        if not hasattr(self, 'entries'):
            return self
        last = self.entries.manager(is_staff).last()
        return last.last_entry(is_staff) if last else self

    def previous(self, is_staff):
        """
        Traverse all the way down your previous sibling's node or,
        if you don't have a previous sibling, go to your parent.
        """
        previous = super(ThreadEntry, self).previous(self.siblings(is_staff))
        return previous.last_entry(is_staff) if previous else self.parent

    def next(self, is_staff):
        """
        To traverse the entry tree, we either get our first entry or, if
        we have no entries, our follower. Our follower is our sibling
        or, failing that, our parent's follower.
        """
        if not hasattr(self, 'entries'):
            return self.follower(is_staff)
        return self.entries.manager(is_staff).first() or self.follower(is_staff)

    def publish_all(self):
        self.publish()
        if hasattr(self, 'entries'):
            for e in self.entries.all():
                e.publish_all()

    def __unicode__(self):
        return self.name



########################################################################
# Main Threads: groups of entries


class Writing(Thread):
    content = models.TextField()

    class Meta(Thread.Meta):
        verbose_name_plural = 'writing'


class WritingEntry(ThreadEntry):
    parent = models.ForeignKey(Writing, related_name='entries')



########################################################################
# Projects: interesting things that I'm working on


class Project(Thread):
    full_phases = (
        ('idea', 'idea', 'project idea'),
        ('design', 'being designed', 'project in design'),
        ('development', 'in development', 'project in development'),
        ('abandoned', 'abandoned', 'abandoned project'),
        ('hiatus', 'on hiatus', 'project on hiatus'),
        ('finished', 'finished', 'finished project'),
        ('public', 'public', 'public project'),
    )
    phases = tuple(p[0] for p in full_phases)
    phase_statuses = tuple(p[1] for p in full_phases)
    phase_descriptions = tuple(p[2] for p in full_phases)
    phase_map = dict((n, i) for (i, n) in enumerate(phases))

    began = models.DateField(default=date.today)
    phase = models.SmallIntegerField(choices=choices(*phases), default=0)
    content = models.TextField()

    def phase_string(self):
        return self.phases[self.phase]

    def phase_status(self):
        return self.phase_statuses[self.phase]

    def phase_description(self):
        return self.phase_descriptions[self.phase]


class ProjectEntry(ThreadEntry):
    parent = models.ForeignKey(Project, related_name='entries')



########################################################################
# Jobs: employment experience etc.


class Job(Thread):
    began = models.DateField(default=date.today)
    ended = models.DateField(blank=True, null=True)

    content = models.TextField()


class JobEntry(ThreadEntry):
    parent = models.ForeignKey(Job, related_name='entries')



########################################################################
# Activities: the things that aren't projects that I do in my free time


class Activity(Thread):
    began = models.DateField(default=date.today)
    ended = models.DateField(blank=True, null=True)

    content = models.TextField()

    class Meta(Thread.Meta):
        verbose_name_plural = 'activities'


class ActivityEntry(ThreadEntry):
    parent = models.ForeignKey(Activity, related_name='entries')



########################################################################
# Tutorials: teaching other people what I know


class Tutorial(Thread):
    content = models.TextField()
    entries = generic.GenericRelation('TutorialSection')


class TutorialSection(ThreadEntry, Ordered):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    parent = generic.GenericForeignKey()
    entries = generic.GenericRelation('self')

    class Meta(Thread.Meta):
        ordering = 'object_id', 'rank'

    def _get_orderer(self):
        return 'rank'

    def informative_name(self):
        return '%s, number %d of %s' % (self.name, self.rank + 1, unicode(self.parent))

    def __unicode__(self):
        return self.name
