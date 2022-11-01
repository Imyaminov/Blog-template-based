from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse_lazy
from .models import Post

# XMLFeed is needed to beautify rss feed xml format
class XMLFeed(Feed):
    def get_feed(self, obj, request):
        feedgen = super().get_feed(obj, request)
        # feedgen.content_type = 'application/rss+xml; charset=utf-8'  # New standard
        feedgen.content_type = 'application/xml; charset=utf-8'  # Old standard, left here for reference
        return feedgen

class LatestPostsFeed(XMLFeed):
    title = "My Blog"
    link = reverse_lazy('blog-home')
    description = 'New posts of my Blog'

    def items(self):
        return Post.objects.all()[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncatewords(item.content, 30)
