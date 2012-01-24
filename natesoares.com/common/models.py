from django.db import models
from personal.utilities.models import Model
from personal.utilities import slugify

class Sluggable(Model):
    slug = models.SlugField(blank=True, unique=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if self.name and not self.slug:
            self.slug = slugify(self.name)
        super(Sluggable, self).save(*args, **kwargs)
