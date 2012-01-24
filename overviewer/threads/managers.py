from django.core.exceptions import FieldError
from django.contrib.contenttypes.models import ContentType
from tags.managers import TagManager, TagQuerySet
import datetime

class PublishableQuerySet(TagQuerySet):
    def published(self):
        from datetime import datetime
        return self.filter(published__lte=datetime.now())

    def manager(self, unpublished=False):
        return self if unpublished else self.published()


class PublishableManager(TagManager):
    def get_query_set(self):
        return PublishableQuerySet(self.model)

    def published(self):
        return self.get_query_set().published()

    def manager(self, unpublished=False):
        return self.get_query_set().manager(unpublished)


class VisibleManager(PublishableManager):
    def get_query_set(self):
        return super(VisibleManager, self).get_query_set().published()


class SubEntryQuerySet(PublishableQuerySet):
    """
    There are two kinds of sub entries. The kinds that know their parent
    (filter parent=parent) and the kind that has a generic foreign key
    to their parent (object_id=parent.id and content_type=parent type).
    """
    def with_parent(self, parent):
        try:
            return self.filter(parent=parent)
        except FieldError:
            type = ContentType.objects.get_for_model(parent)
            return self.filter(object_id=parent.id, content_type=type)


class SubEntryManager(PublishableManager):
    def get_query_set(self):
        return SubEntryQuerySet(self.model)

    def with_parent(self, parent):
        return self.get_query_set().with_parent(parent)


class VisibleSubEntryManager(SubEntryManager):
    def get_query_set(self):
        return super(VisibleSubEntryManager, self).get_query_set().published()
