from django.contrib.syndication.feeds import Feed
from django.core.exceptions import ObjectDoesNotExist
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from overviewer.utilities.functional import take
from overviewer.threads.views import sections, section_map
from itertools import chain

LIMIT = 8

class NateFeed(Feed):
    author_name = 'Nathaniel Soares'
    author_email = 'contact@natesoares.com'


def section_feeds(section):
    class SectionFeed(NateFeed):
        description_template = 'feeds/description.html'
        title = 'NateSoares.com %s updates' % section.model.single()
        description = 'Updates and additions to NateSoares.com %s' % section.model.root()

        def link(self):
            return reverse(section.default)

        def items(self):
            return section.model.objects.all()[:LIMIT]

    class AtomSectionFeed(SectionFeed):
        feed_type = Atom1Feed
        subtitle = SectionFeed.description

    return AtomSectionFeed, SectionFeed


class AllFeed(NateFeed):
    feed_type = Atom1Feed
    title = 'NateSoares.com updates to all sections'
    description = 'All new entries and sub-entries in all sections of NateSoares.com'
    subtitle = description

    def link(self):
        return reverse(sections[0].default)

    def items(self):
        sorter = lambda x, y: -cmp(x.published, y.published)
        items = chain(*(s.all_relevant(limit=LIMIT) for s in sections))
        return take(LIMIT, sorted(items, sorter))



class EntryFeed(NateFeed):
    feed_type = Atom1Feed

    def get_object(self, bits):
        try:
            section, slug = bits
        except ValueError:
            raise ObjectDoesNotExist
        try:
            self.section = section_map[section]
        except KeyError:
            raise ObjectDoesNotExist
        return self.section.model.objects.get(slug=slug)

    def title(self, object):
        return 'NateSoares.com entries for %s' % object

    def link(self, object):
        return object.get_absolute_url()

    def description(self, object):
        return 'Recent entries added to %s' % object
    subtitle = description

    def items(self, object):
        if hasattr(object, 'traverse'):
            sorter = lambda x, y: -cmp(x.published, y.published)
            return take(LIMIT, sorted(object.traverse(), sorter))
        return object.entries.manager().all()[:LIMIT]


feeds = {'all': AllFeed, 'entries': EntryFeed}
for section in sections:
    (atom, rss) = section_feeds(section)
    feeds[str(section)] = atom
    feeds['%s-rss' % section] = rss
