import datetime
import os
import sys
import urllib
from functools import lru_cache

import bangla
import pdfkit
from asgiref.sync import sync_to_async
from dateutil.relativedelta import *
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import translation
from django.utils.functional import keep_lazy
from django.views.decorators.cache import cache_page
from django.views.decorators.http import require_GET
from PIL import Image, ImageDraw, ImageFont, ImageOps

from discord_custom import *

from .models import *
from .templatetags.extra import get_latest_video


@login_required
@sync_to_async
@cache_page(60 * 15)
def user_logout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out!")
    return redirect(reverse("Home"))


@sync_to_async
@cache_page(60 * 15)
def changelang(request):
    old_lang = translation.to_locale(translation.get_language())
    l = (request.META.get("HTTP_REFERER")
         if request.META.get("HTTP_REFERER") else reverse("Home"))
    if old_lang == "en":
        translation.activate("bn")
        return redirect(l.replace("en", "bn"))
    translation.activate("en")
    return redirect(l.replace("bn", "en"))


# Images Api, which generates the cards images


@require_GET
@cache_page(60 * 15)
def getimages(request):
    return HttpResponse(generate_thumbnail(request), content_type="image/jpeg")


# Create your views here.
@sync_to_async
@cache_page(60 * 15)
def homeredirect(request):
    return redirect(reverse("Home"))


@require_GET
@sync_to_async
@cache_page(60 * 15)
def schedule(request, year):
    name1 = f"Durga Puja Schedule for {year}"
    try:
        year_model, show = Year.objects.filter(year=int(year)).get(), True
    except Year.DoesNotExist:
        raise Http404("Nothing in this year as of now")

    params = {
        "year": year_model,
        "show": show,
        "title": name1,
        "view": "schedule",
        "year_year": year,
        "yearpassed": year,
        "current_year_puja": keep_lazy(int(durgapujayear()), int),
    }

    return render(request, "schedule.html", params)


@require_GET
@sync_to_async
@cache_page(60 * 15)
def scheduleprint(request, year, one: int = None):
    try:
        year_model = Year.objects.filter(year=year).get()
    except Year.DoesNotExist:
        raise Http404("Nothing in this year as of now")

    params = {
        "year": year_model,
        "yearpassed": year,
        "view": "schedule",
        "title": f"Durga Puja Schedule for {year}",
        "one": one != 1,
        "current_year_puja": keep_lazy(durgapujayear()),
    }

    return render(request, "schedulepdf.html", params)


@cache_page(60 * 15)
def schedulepdf(request, year):
    try:
        yearobj = Year.objects.filter(year=year).get()
    except Year.DoesNotExist:
        raise Http404("Nothing in this year as of now")

    current_site = get_current_site(request)
    domain = current_site.domain

    if sys.platform.startswith("win32"):
        if os.environ.get("ASYNC_RUN"):
            return HttpResponse("This can run only in sync only mode! :)",
                                status=503)
        if os.path.isdir(os.path.join(settings.MEDIA_ROOT, "pdf")):
            pass
        else:
            os.mkdir(os.path.join(settings.MEDIA_ROOT, "pdf"))
        config = pdfkit.configuration(
            wkhtmltopdf=settings.BASE_DIR /
            os.path.join("wkhtmltopdf", "bin", "wkhtmltopdf.exe"))
        pdfkit.from_url(
            f"http://{domain}{reverse('schedule print',args=[year])}",
            False,
            configuration=config,
        )

        with open(
                os.path.join(settings.MEDIA_ROOT, "pdf",
                             f"schedulepdf-{year}.pdf"), "rb") as pdf_file:
            data = pdf_file.read()
        sync_to_async(
            os.remove(
                os.path.join(settings.MEDIA_ROOT, "pdf",
                             f"schedulepdf-{year}.pdf")))
        filename = f"schedulepdf-{year}.pdf"
        content_type = "application/pdf"

    else:
        if os.path.isdir(os.path.join(settings.MEDIA_ROOT, "img")):
            pass
        else:
            os.mkdir(os.path.join(settings.MEDIA_ROOT, "img"))
        img = urllib.request.urlopen(
            f'https://image.thum.io/get/width/1920/crop/900/maxAge/1/noanimate/http://{domain+reverse("schedule img",args=[year, 1])}'
        ).read()

        with open(settings.MEDIA_ROOT / f"schedulepdf-{year}.png",
                  "wb") as img_file:
            img_file.write(img)
        with open(settings.MEDIA_ROOT / f"schedulepdf-{year}.png",
                  "rb") as img_file:
            data = img_file.read()
        sync_to_async(
            os.remove(settings.MEDIA_ROOT / f"schedulepdf-{year}.png"))

        filename = f"schedulepdf-{year}.png"
        content_type = "image/png"

    response = HttpResponse(data, content_type=content_type)
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


@require_GET
@sync_to_async
def home(request):

    name1 = "Videos List"
    year = Year.objects.all()
    videos = (Videos.objects.filter(
        test=False).select_related("yearmodel").distinct("yearmodel"))
    videoslive = (Videos.objects.select_related("yearmodel").values(
        "yearmodel", "live").filter(live=True, test=False))

    page = request.GET.get("page", 1)
    paginator = Paginator(year, 6)

    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(
        request,
        "playlist.html",
        {
            "yearmodel": page_obj,
            "videos": videos,
            "title": name1,
            "view": "Home",
            "videoslive": videoslive,
            "current_year_puja": keep_lazy(durgapujayear()),
        },
    )


@require_GET
@sync_to_async
@cache_page(60 * 15)
def video(request, year, day):
    try:
        yearid = Year.objects.values("id").filter(year=int(year)).get()["id"]
    except:
        raise Http404("The year in our database does not exist!")

    day = day.upper()
    if day in ("E", "DI", "T", "C", "P"):
        return redirect(reverse("Videos", args=[int(year), "MAA"]))
    if day == "S":
        dayname = "Shashti"
    elif day == "SA":
        dayname = "Sapatami"
    elif day == "A":
        dayname = "Ashtami"
    elif day == "SAN":
        dayname = "Sandhi"
    elif day == "N":
        dayname = "Navami"
    elif day == "D":
        dayname = "Dashami"
    elif day == "MAA":
        try:
            maahome = (Year.objects.filter(
                year=int(year)).values("maacomevid").get()["maacomevid"])
        except IndexError:
            return redirect(reverse("Videos", args=[int(year), "S"]))
        if not maahome:
            raise Http404("The day you requested in not available")
    else:
        raise Http404("The day you requested in not available")

    if day == "MAA":
        videos = Videos.objects.filter(yearmodel=yearid,
                                       day__in=["E", "DI", "T", "C", "P"],
                                       test=False).select_related("yearmodel")
        try:
            day = videos[0].day
        except IndexError:
            return redirect(reverse("Videos", args=[int(year), "S"]))
        if day == "E":
            dayname = "Ekami"
        elif day == "DI":
            dayname = "Dvutia"
        elif day == "T":
            dayname = "Tritiya"
        elif day == "C":
            dayname = "Chathurti"
        elif day == "P":
            dayname = "Panchami"
    else:
        videos = Videos.objects.filter(yearmodel=yearid, day=day,
                                       test=False).all()
    show = not videos.count() <= 0

    livevideo = (Videos.objects.filter(yearmodel=yearid, live=True,
                                       test=False).values("day",
                                                          "live").exists())
    if not livevideo:
        livevideo = Videos.objects.none()

    maahome = (Year.objects.filter(
        year=int(year)).values("maacomevid").get()["maacomevid"])

    return render(
        request,
        "videos.html",
        {
            "videos": videos,
            "title": f"Maha {dayname}",
            "yearpassed": year,
            "dayname": dayname.upper(),
            "lengthday": len(dayname),
            "view": "",
            "livevideo": livevideo,
            "show": show,
            "maahome": maahome,
            "day": day,
            "current_year_puja": keep_lazy(durgapujayear()),
        },
    )


@require_GET
@sync_to_async
@cache_page(60 * 15)
def about_year(request, year):
    try:
        yearid = Year.objects.filter(year=int(year)).get()
    except:
        raise Http404("The year in our database does not exist!")
    img_dir = os.listdir(settings.BASE_DIR /
                         os.path.join("main", "static", "img"))

    def addimg(a):
        return "img/" + a

    return render(
        request,
        "about_year.html",
        {
            "yearpassed": year,
            "title": f"About the year puja {year}",
            "year": yearid,
            "view": "about",
            "img_dir": list(map(addimg, img_dir)),
            "current_year_puja": keep_lazy(durgapujayear()),
        },
    )


@sync_to_async
@cache_page(60 * 15)
def redirect_view_puja(request):
    # Year
    x = datetime.datetime.now()
    year = x.strftime("%Y")
    try:
        yearid = Year.objects.values("id").filter(year=int(year)).get()["id"]
    except Year.DoesNotExist:
        yearid = None
        return redirect(reverse("Home"))

    # Day requiring
    try:
        videodict = (Videos.objects.filter(
            yearmodel=yearid, live=True,
            test=False).select_related("yearmodel").values("day").get())
    except:
        videodict = {"day": "None"}
        try:
            videodict = (Videos.objects.filter(
                yearmodel=yearid,
                test=False).select_related("yearmodel").values("day").latest(
                    "yearmodel", "day"))
        except Exception as e:
            return redirect(reverse("Home"))

    # redirecting the user to the correct page
    return redirect(
        reverse("Videos", args=[int(year), videodict["day"]]) + "#live")


@sync_to_async
@cache_page(60 * 15)
def qrcode(request, logo=2):
    from .qrcode_gen import QrGen

    current_site = get_current_site(request)
    domain = current_site.domain
    return HttpResponse(
        QrGen("https://" + domain + reverse("Redirect"),
              logo == 1).gen_qr_code(),
        content_type="image/jpeg",
    )


@cache_page(60 * 15)
def handler404(request, *args, **argv):
    x = datetime.datetime.now()
    return render(
        request,
        "exception_status.html",
        {
            "title": "404 Ohh Snap!!! Sorry!",
            "exception_status": 400,
            "yearpassed": int(x.strftime("%Y")),
            "current_year_puja": keep_lazy(durgapujayear()),
            "system_message": argv.get("exception"),
        },
    )


@cache_page(60 * 15)
def handler500(request, *args, **argv):
    embed = Embed(
        title="Error",
        color=Color.red(),
    )
    embed.description = "```args: {}```\n\nargv: {}```".format(args, argv)
    discord_api_req(
        path=settings.SENTRY_URL,
        method="post",
        data={
            "content":
            "<@887549958931247137>",
            "embeds": [embed.to_dict()],
            "allowed_mentions":
            AllowedMentions(everyone=True, roles=True, users=True).to_dict(),
        },
    )
    x = datetime.datetime.now()
    return render(
        request,
        "exception_status.html",
        {
            "title": "500 Ohh Snap!!! Sorry!",
            "exception_status": 500,
            "yearpassed": int(x.strftime("%Y")),
            "system_message": argv.get("exception"),
        },
    )


@lru_cache
def durgapujayear():
    return relativedelta(datetime.datetime.now(),
                         datetime.datetime(2001, 1, 1)).years


@lru_cache
def generate_thumbnail(request_obj):
    request = request_obj
    if os.path.isdir(os.path.join(settings.MEDIA_ROOT, "yearpic")):
        pass
    else:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, "yearpic"))

    text = request.GET["text"]
    back = request.GET.get("back", "#FFF00C")
    textc = request.GET.get("textc", "#496d89")

    img = Image.new("RGBA", (100, 30), color=str(back))
    d = ImageDraw.Draw(img)
    w, h = d.textsize(str(text))

    if request.LANGUAGE_CODE == "bn" and text.replace("/", "").isdigit():
        font = os.path.join(settings.BASE_DIR, "main", "static", "fonts",
                            "Baloo_Da-Regular.ttf")
        text = bangla.convert_english_digit_to_bangla_digit(str(text))
        d.text(
            ((100 - w) / 2, (25 - h) / 2),
            str(text),
            fill=str(textc),
            font=ImageFont.truetype(font,
                                    11,
                                    layout_engine=ImageFont.LAYOUT_RAQM),
        )
    else:
        d.text(((100 - w) / 2, (30 - h) / 2), str(text), fill=str(textc))

    output_image = os.path.join(settings.MEDIA_ROOT, "yearpic",
                                str(text) + "output" + ".png")
    main_image = os.path.join(settings.MEDIA_ROOT, "yearpic",
                              str(text) + ".png")

    # Try Except Block
    output_image1 = output_image
    try:
        img.save(output_image1)
    except:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, "yearpic"))
        img.save(output_image1)

    # Making the image circular
    mask = Image.open(
        os.path.join(settings.BASE_DIR, "main", "imagesreq",
                     "mask.png")).convert("L")
    im = Image.open(output_image)

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    # Saving the cropped Image
    output.save(main_image)
    with open(main_image, "rb") as image_file:
        image_data = image_file.read()
    # Deleting the first image made
    sync_to_async(os.remove(output_image1))
    sync_to_async(os.remove(main_image))
    return image_data


@sync_to_async
@cache_page(60 * 15)
def serve_arc(request):
    return render(request, "arc-sw.js", content_type="application/javascript")


@sync_to_async
@cache_page(60 * 15)
def serve_auth_dns(request):
    return render(request,
                  "3381C685CDBA944E82A7AE6F1444D4D2.txt",
                  content_type="text/plain")
