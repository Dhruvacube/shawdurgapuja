from django.contrib.syndication.views import Feed
from django.utils import timezone
from django.urls import reverse_lazy

from .models import *


class YearFeed(Feed):
    title = "Latest Puja Videos"
    description = "Get the all the latest puja videos sorted Year-wise"
    link = reverse_lazy("Redirect")

    def get_object(self, request, *args, **kwargs):
        return Year.objects.all()

    def title(obj):
        return f"YEAR - {obj.year}"

    def description(obj):
        return obj.yeardesc or f"See all the puja videos of the YEAR {obj.year}"

    def items(obj):
        return Videos.objects.filter(yearmodel=obj.id, test=False).order_by(
            "-yearmodel"
        )

    def item_copyright():
        return "Copyright (c) 2019, Shaw Durga Puja"
