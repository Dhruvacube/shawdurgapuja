from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path, register_converter
from django.utils.translation import gettext_lazy as _

from main import converters
from main.rss_feed import YearFeed
from main.views import *

from .sitemaps import StaticViewSitemap

sitemaps = {"static": StaticViewSitemap}

register_converter(converters.FourDigitYearConverter, "yyyy")

urlpatterns = [
    # path(".well-known/pki-validation/3381C685CDBA944E82A7AE6F1444D4D2.txt", serve_auth_dns, name="Verify SSL Records"),
    path("arc-sw.js", serve_arc, name="Arc.io serve js"),
    path("admin/doc/", include("django.contrib.admindocs.urls")),
    path("admin/", admin.site.urls),
    re_path(r"^logout/$", user_logout, name="signout"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="Sitemap"),
    path("qrcode/", qrcode, name="QrcodeGen"),
    path("qrcode/<int:logo>/", qrcode, name="QrcodeGenLogo"),
    path("redirect/", redirect_view_puja, name="Redirect"),
    path("", homeredirect, name="HomeRedirect"),
]

urlpatterns = (
    i18n_patterns(
        path(_(""), home, name="Home"),
        path(_("videos/<yyyy:year>/<str:day>"), video, name="Videos"),
        path(_("aboutyear/<yyyy:year>"), about_year, name="About Year"),
        path(_("schedule/<yyyy:year>/"), schedule, name="schedule"),
        path(_("scheduleprint/<yyyy:year>/"),
             scheduleprint, name="schedule print"),
        path(
            _("scheduleimg/<yyyy:year>/<int:one>"), scheduleprint, name="schedule img"
        ),
        path(_("schedulepdf/<yyyy:year>/"), schedulepdf, name="schedule pdf"),
        re_path(_(r"^rss/latest$"), YearFeed(), name="RSS"),
        path(_("redirect/"), redirect_view_puja, name="Redirect"),
        re_path(_(r"^getimages$"), getimages, name="GetImages"),
        path(_("changelang/"), changelang, name="ChangeLang"),
    )
    + urlpatterns
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

handler404 = "main.views.handler404"
handler500 = "main.views.handler500"
