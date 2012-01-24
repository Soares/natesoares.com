from datetime import date
from django.db import models
from personal.tags.models import Taggable
from personal.tags.managers import TagManager
from personal.common.models import Sluggable
from personal.common.managers import PublishedTagManager
from personal.projects.managers import ActiveManager

phases = (
    ('i', 'Idea'),
    ('d', 'Design'),
    ('D', 'Development'),
    ('h', 'Hiatus'),
    ('a', 'Abandoned'),
    ('f', 'Finished'),
    ('p', 'Public'),
)


class Project(Sluggable, Taggable):
    name = models.CharField(max_length=255)
    brief = models.CharField(max_length=255, blank=True)
    phase = models.CharField(max_length=1, choices=phases, default=0)
    began = models.DateField(default=date.today)
    description = models.TextField()

    published = models.DateTimeField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    all_objects = TagManager()
    objects = PublishedTagManager()
    active = ActiveManager()

    class Meta:
        ordering = 'phase', 'name'

    def get_absolute_url(self):
        return '/projects/%s/' % self.slug

    def __unicode__(self):
        return self.name
