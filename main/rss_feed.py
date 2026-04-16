from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils import timezone

from .models import *


class YearFeed(Feed):
    title = "Latest Puja Videos"
    description = "Get the all the latest puja videos sorted Year-wise"
    link = reverse_lazy("Redirect")

    def items(self):
        return Videos.objects.filter(test=False).select_related("yearmodel").order_by("-yearmodel__year", "-id")

    def item_title(self, item):
        return f"YEAR - {item.yearmodel.year} - {item.streamingvideoheader}"

    def item_description(self, item):
        return item.streamingvideodescription or f"See the puja video of the YEAR {item.yearmodel.year}"

    def item_copyright(self):
        return "Copyright (c) 2019, Shaw Durga Puja"
