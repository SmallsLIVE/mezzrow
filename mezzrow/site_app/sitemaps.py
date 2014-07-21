from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from smallslive.events.models import Event


class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'monthly'

    def items(self):
        return ['about', 'contact']

    def location(self, obj):
        return reverse(obj)


class EventListSitemap(sitemaps.Sitemap):
    priority = 0.6
    changefreq = 'daily'

    def items(self):
        return ['home', 'events_month', 'events_year']

    def location(self, obj):
        return reverse(obj)


class EventDetailSitemap(sitemaps.Sitemap):
    priority = 0.8
    changefreq = "daily"

    def items(self):
        return Event.objects.filter(state=Event.STATUS.Published)

    def lastmod(self, obj):
        return obj.modified
