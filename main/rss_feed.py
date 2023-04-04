from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy

from .models import *


class YearFeed(Feed):
    title = "Latest Puja Videos"
    description = "Get the all the latest puja videos sorted Year-wise"
    link = reverse_lazy("Redirect")

    def get_object(self, request, *args, **kwargs):
        return Year.objects.all()

    @staticmethod
    def title(obj):
        return f"YEAR - {obj[0].year}"

    @staticmethod
    def description(obj):
        return obj[0].yeardesc or f"See all the puja videos of the YEAR {obj[0].year}"

    @staticmethod
    def items(obj):
        return Videos.objects.filter(yearmodel=obj[0].id, test=False).order_by(
            "-yearmodel"
        )

    @staticmethod
    def item_copyright():
        return "Copyright (c) 2019, Shaw Durga Puja"
