from core.models import Problem

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings

from datetime import date, time, datetime
from pytz import timezone


class rss_feed(Feed):
    title = "Problem of the Day"
    link = "/blog/"
    description = "Latest problems from Problem of the Day"

    def items(self):
        return Problem.objects.filter(date__lte=date.today())[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.text

    def item_pubdate(self, item):
        return datetime.combine(item.date, time(tzinfo=timezone(settings.TIME_ZONE)))


class atom_feed(rss_feed):
    feed_type = Atom1Feed
    subtitle = rss_feed.description
