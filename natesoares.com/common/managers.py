from datetime import datetime
from personal.utilities.managers import QuerySet, Manager
from personal.tags.managers import TagQuerySet, TagManager

class PublishedQuerySet(QuerySet):
    def published(self):
        return self.filter(published__isnull=False).filter(published__lte=datetime.now())


class PublishedManager(Manager):
    def get_query_set(self):
        return PublishedQuerySet(self.model)

    def published(self):
        return self.get_query_set().published()


class PublishedTagQuerySet(TagQuerySet, PublishedQuerySet):
    pass


class PublishedTagManager(TagManager, PublishedManager):
    def get_query_set(self):
        return PublishedTagQuerySet(self.model).published()
