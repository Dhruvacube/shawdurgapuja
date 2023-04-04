import json
from typing import Literal
from urllib import request

from django.conf import settings


def discord_api_req(
    path: str,
    method: Literal["GET", "POST", "PUT", "PATCH", "DELETE"],
    data=None,
    content_type: str = "application/json",
):
    base_api = "https://discord.com/api"
    headers = {
        "User-Agent": "Shaw Durga Puja Website",
        "X-Ratelimit-Precision": "millisecond",
        "Authorization": f"Bot {settings.TOKEN}",
        "Content-Type": content_type,
    }
    req = request.Request(url=base_api + path,
                          headers=headers, method=method.upper())
    if data:
        data = json.dumps(data)
        data = data.encode()
    r = request.urlopen(req, data=data)
    content = r.read()
    return content
