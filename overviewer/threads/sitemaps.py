from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from overviewer.threads.views import sections, start_date
from datetime import datetime, timedelta
from itertools import chain

daily = timedelta(4)
weekly = timedelta(16)
monthly = timedelta(128)


class ListSitemap(Sitemap):
    changefreq = 'daily'

    def items(self):
        return sections

    def lastmod(self, section):
        first = section.model.objects.order_by('-updated').first()
        return first.updated if first else start_date

    def priority(self, section):
        return 0.3 if not section.private else 0.2


class ArchiveSitemap(ListSitemap):
    def location(self, section):
        return reverse(section.archives)


class ListingSitemap(ListSitemap):
    def location(self, section):
        return reverse(section.listing)


def section_sitemap(section):
    class SectionSitemap(Sitemap):
        def items(self):
            return list(section.all_relevant())

        def changefreq(self, item):
            delta = datetime.now() - item.published
            if delta <= daily:
                return 'daily'
            elif delta <= weekly:
                return 'weekly'
            elif delta <= monthly:
                return 'monthly'
            return yearly

        def priority(self, item):
            if section.private:
                return 0.8 if isinstance(item, section.model) else 0.6
            return 0.9 if isinstance(item, section.model) else 0.7

        def lastmod(self, item):
            return item.updated
    return SectionSitemap


sitemaps = dict((str(s), section_sitemap(s)) for s in sections)
sitemaps['archives'] = ArchiveSitemap
sitemaps['listing'] = ListingSitemap
