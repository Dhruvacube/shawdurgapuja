import os

import pyqrcode
from asgiref.sync import sync_to_async
from django.conf import settings
from PIL import Image


class QrGen:
    def __init__(self, data: str, logo: bool = True):
        self.data = data
        self.logo = logo
        self.files_logo = os.path.join(
            settings.BASE_DIR, "main", "static", "assets", "img", "default_qrcode.png"
        )

    def gen_qr_code(self):
        filename = "with_logo.png" if self.files_logo else "withoutout_logo.png"

        url = pyqrcode.QRCode(self.data, error="H")
        url.png(os.path.join(settings.BASE_DIR, "main", filename), scale=10)

        im = Image.open(os.path.join(settings.BASE_DIR, "main", filename))
        im = im.convert("RGBA")
        im.save(os.path.join(settings.BASE_DIR, "main", filename), scale=10)

        if self.logo:
            logo1 = Image.open(self.files_logo)
            width, height = im.size

            # How big the logo we want to put in the qr code png
            logo_size = 100

            # Calculate xmin, ymin, xmax, ymax to put the logo
            xmin = ymin = int((width / 2) - (logo_size / 2))
            xmax = ymax = int((width / 2) + (logo_size / 2))

            region = logo1
            region = region.resize((xmax - xmin, ymax - ymin))
            im.paste(region, (xmin, ymin, xmax, ymax))

            im.save(os.path.join(settings.BASE_DIR, "main", filename), scale=10)

        with open(os.path.join(settings.BASE_DIR, "main", filename), "rb") as f:
            data = f.read()
        sync_to_async(os.remove(os.path.join(
            settings.BASE_DIR, "main", filename)))
        return data
