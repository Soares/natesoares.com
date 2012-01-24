from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed
from personal.writing.models import Entry
from personal.utilities.views import top, top_changes

class CommonFeed(Feed):
    description_template = '/feeds/description.html'


class LatestEntries(CommonFeed):
    title = "Nate's Thoughts"
    link = '/writing/'
    description = 'New entries on NateSoares.com'

    def items(self):
        return Entry.objects.order_by('-published')[:8]


class LatestUpdates(CommonFeed):
    title = "Nate's Updates"
    link = '/updates/'
    description = 'New major updates to NateSoares.com, from writing to projects to activities and more'

    def items(self):
        return top(8)


class LatestChanges(CommonFeed):
    title = "Nate's Changes"
    link = '/changes/'
    description = 'New annotations, changes, addendums, and notes that nobody cares about on NateSoares.com'

    def items(self):
        return top_changes(8)


class AtomConverter(object):
    feed_type = Atom1Feed
    subtitle = property(lambda self: super(AtomConverter, self).description)


class AtomLatestEntries(AtomConverter, LatestEntries):
    pass


class AtomLatestUpdates(AtomConverter, LatestUpdates):
    pass


class AtomLatestChanges(AtomConverter, LatestChanges):
    pass
