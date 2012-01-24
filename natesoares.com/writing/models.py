from django.db import models
from personal.tags.models import Taggable
from personal.common.models import Sluggable
from personal.writing.managers import EntryManager, VisibleManager

class Entry(Sluggable, Taggable):
    name = models.CharField(max_length=255)
    brief = models.CharField(max_length=255, blank=True)
    published = models.DateTimeField(blank=True, null=True)
    content = models.TextField()
    summary = models.TextField(blank=True)

    projects = models.ManyToManyField('projects.Project', blank=True, related_name='writing')
    activities = models.ManyToManyField('activities.Activity', blank=True, related_name='writing')
    jobs = models.ManyToManyField('jobs.Job', blank=True, related_name='writing')

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    all_objects = EntryManager()
    objects = VisibleManager()

    class Meta:
        ordering = '-created',
        verbose_name_plural = 'entries'

    def get_absolute_url(self):
        return '/writing/%s/' % self.slug

    def __unicode__(self):
        return self.name
