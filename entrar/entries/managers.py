from utilities.managers import Manager
from functools import partial

class EntryManager(Manager):
    def __get_entry(self, slug, commit=True):
        entry, created = self.model.objects.get_or_create(slug=slug, defaults={
            'name': slug, 'content': '',
        })
        if commit and created:
            entry.save()
        return entry

    def get_entries(self, *slugs, **kwargs):
        commit = kwargs.get('commit', True)
        return map(partial(self.__get_entry, commit=commit), slugs)
