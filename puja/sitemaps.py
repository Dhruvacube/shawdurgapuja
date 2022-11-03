from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from main.models import Year


class StaticViewSitemap(Sitemap):
    changefreq = "yearly"

    @staticmethod
    def priority(item):
        return 1.0 if item[0] in ("H", "s", "R") else 0.80

    def items(self):
        year, l = Year.objects.values("year").all(), []
        for i in year:
            l.extend(
                [
                    f'Videos/{i["year"]}/{day}'
                    for day in ["S", "SA", "A", "SAN", "N", "D"]
                ]
                + [f'schedule/{i["year"]}', f'About Year/{i["year"]}']
            )
        return ["Home", "Redirect"] + l

    def location(self, item):
        if item in ("Home", "Redirect"):
            return reverse(item)
        if item[0].lower() in ("s", "A", "a", "Y"):
            return reverse(str(item.split("/")[0]), args=[int(item.split("/")[1])])
        return reverse(
            str(item.split("/")[0]),
            args=[int(item.split("/")[1]), item.split("/")[2]],
        )
