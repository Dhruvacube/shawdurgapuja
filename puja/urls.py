from django.conf import settings
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, register_converter
from django.utils.translation import gettext_lazy as _
from main import converters
from main.views import *

from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap
}

register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [

    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),

    url(r'^logout/$', user_logout, name='signout'),
    path('schedulepdf/<yyyy:year>/',schedulepdf,name="schedule pdf"),
    
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    
    path('', homeredirect,name="HomeRedirect"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns = i18n_patterns(
    path(_(''), home,name="Home"),
    path(_('videos/<yyyy:year>/<str:day>'),video,name="Videos"),
    path(_('aboutyear/<yyyy:year>'),about_year,name="About Year"),
    path(_('schedule/<yyyy:year>/'),schedule,name="schedule"),
    path(_('scheduleprint/<yyyy:year>/'),scheduleprint,name="schedule print"),
    
    path(_('redirect/'), redirect_view_puja,name="Redirect"),
    url(_(r'^getimages$'), getimages, name="GetImages"),
    path(_('changelang/'), changelang, name='ChangeLang'),
) + urlpatterns

handler404 = 'main.views.handler404'
handler500 = 'main.views.handler500'
