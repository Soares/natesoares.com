from datetime import date
from django.db import models
from personal.tags.models import Taggable
from personal.tags.managers import TagManager
from personal.common.models import Sluggable
from personal.common.managers import PublishedTagManager

class Job(Sluggable, Taggable):
    name = models.CharField(max_length=255)
    brief = models.CharField(max_length=255, blank=True)
    added = models.DateField(auto_now_add=True)
    began = models.DateField(default=date.today)
    ended = models.DateField(blank=True, null=True)
    summary = models.TextField()

    published = models.DateTimeField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    all_objects = TagManager()
    objects = PublishedTagManager()

    class Meta:
        ordering = '-began',

    def get_absolute_url(self):
        return '/jobs/%s/' % self.slug

    def __unicode__(self):
        return self.name
