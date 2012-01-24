from managers import Manager
from django.db import models
from django.shortcuts import _get_queryset

def choices(*args):
    return tuple(enumerate(args))


class Ordered(models.Model):

    class Meta:
        abstract = True

    def _get_orderer(self):
        return self._meta.ordering[0].lstrip('-')

    def _filter(self, direction, objects):
        field = self._get_orderer()
        objects = objects or self.__class__._default_manager
        rank = getattr(self, field)
        if rank is None:
            return objects.order_by(field)
        description = {'%s__%s' % (field, direction): rank}
        return objects.filter(**description).order_by(field)

    def after(self, objects):
        return self._filter('gt', objects)

    def before(self, objects):
        return self._filter('lt', objects)

    def first(self, objects=None):
        print objects, self, self.before(objects)
        return self.before(objects).first()

    def previous(self, objects=None):
        return self.before(objects).last()

    def next(self, objects=None):
        return self.after(objects).first()

    def newest(self, objects=None):
        return self.after(objects).last()
