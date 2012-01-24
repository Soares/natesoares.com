from lexer import slugs, lex
from managers import EntryManager
from django.db import models
from django.utils.safestring import mark_safe
from markdown2 import markdown


class Entry(models.Model):
    """
    Notice that there is nothing in the hat ...

    >>> entries = Entry.objects.filter(slug__in=('entry1', 'entry2', 'entry3'))
    >>> entries.count()
    0

    Calling get_entries returns a list of entries in the order
    of the arguments passed.

    >>> Entry.objects.get_entries('entry1', 'entry2')
    [<Entry: entry1>, <Entry: entry2>]

    By default, calling get_entries saves the new entry 

    >>> Entry.objects.get(slug='entry1')
    <Entry: entry1>

    Get_entries is indempotent, and if the entry already exists
    you will get no errors

    >>> Entry.objects.get_entries('entry2')
    [<Entry: entry2>]

    It is possible to call get_entries with commit=False

    >>> Entry.objects.get_entries('entry3', commit=False)
    [<Entry: entry3>]

    In this case, new entries will not be saved

    >>> hasattr(Entry.objects.get(slug='entry3'), 'id')
    False

    Cleanup

    >>> for e in entries:
    ...     e.delete()
    """
    slug = models.SlugField(primary_key=True)
    outgoing = models.ManyToManyField('self', symmetrical=False, related_name='incoming')

    name = models.CharField(max_length=128)
    brief = models.CharField(max_length=255, blank=True)
    content = models.TextField()

    updated = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    next = models.ForeignKey('self', blank=True, null=True,
                             related_name='previous_set')

    objects = EntryManager()

    class Meta:
        ordering = 'name',
        verbose_name_plural = 'entries'

    @property
    def previous(self):
        if not hasattr(self, '_previous'):
            self._previous = self.previous_set.first()
        return self._previous

    def save(self, *args, **kwargs):
        self.outgoing = self.__class__.objects.get_entries(*slugs(self.content))
        super(Entry, self).save(*args, **kwargs)

    def publish(self):
        self.published = True
        super(Entry, self).save()

    def pull(self):
        self.published = False
        super(Entry, self).save()

    def is_stub(self):
        return not (self.content and self.published)

    def shown_to(self, user):
        return self.published or user.is_staff

    def render(self):
        stubs = dict((o.slug, True) for o in self.outgoing.all() if o.is_stub())
        return mark_safe(markdown(lex(self.content, stubs)))

    def real_outgoing(self):
        for out in self.outgoing.all():
            if not out.is_stub():
                yield out

    @models.permalink
    def get_absolute_url(self):
        return 'entries.views.entry', [self.slug]

    def __unicode__(self):
        return '%s%s' % (self.name, ' (stub)' if self.is_stub() else '')
