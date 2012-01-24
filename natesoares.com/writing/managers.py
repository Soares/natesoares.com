from personal.common.managers import PublishedTagQuerySet, PublishedTagManager

class EntryQuerySet(PublishedTagQuerySet):
    def nearby(self, **identifier):
        entry = self.get(**identifier)
        after = self.filter(created__gt=entry.created).order_by('created')
        before = self.filter(created__lt=entry.created).order_by('-created')

        newest = after.empty()
        oldest = before.empty()

        first = before.reverse()[0] if not oldest else None
        previous = before[0] if not oldest else None
        next = after[0] if not newest else None
        latest = after.reverse()[0] if not newest else None

        return first, previous, next, latest


class EntryManager(PublishedTagManager):
    def get_query_set(self):
        return EntryQuerySet(self.model)

    def nearby(self, **identifier):
        return self.get_query_set().nearby(**identifier)


class VisibleManager(EntryManager):
    def get_query_set(self):
        return super(VisibleManager, self).get_query_set().published().order_by('-published')
