from personal.utilities.managers import Manager
from django.db import models


class Model(models.Model):
    objects = Manager()

    class Meta:
        abstract = True
