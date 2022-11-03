from typing import Iterable, Iterator, Optional, Union

from django import template

register = template.Library()


@register.filter
def get_latest_video(queryset: Union[Iterable, Iterator], year: int) -> Optional[str]:
    for i in queryset:
        if i.yearmodel.year == year:
            return i
