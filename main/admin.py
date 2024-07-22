from django.contrib import admin, messages
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import Group
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext
from django_admin_listfilter_dropdown.filters import (
    ChoiceDropdownFilter,
    DropdownFilter,
    RelatedDropdownFilter,
)

from .models import Videos, Year

# Register your models here.


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = (
        "year",
        "shashti",
        "saptami",
        "ashtami",
        "sandhi",
        "navami",
        "dashami",
    )
    list_filter = (("year", DropdownFilter), )
    search_fields = list_display + ("yeardesc", )
    list_per_page = 30

    fieldsets = (
        (_("Year"), {
            "fields": ("year", )
        }),
        (_("Year Description"), {
            "fields": ("yeardesc", )
        }),
        (_("Pictures of Background"), {
            "fields": ("colourback", "colourtext")
        }),
        (
            _("Live Video of Maa Durga coming from potuapara to Home"),
            {
                "fields": ("maacomevid", )
            },
        ),
        (
            _("Puja Dates"),
            {
                "fields": (
                    "shashti",
                    "saptami",
                    "ashtami",
                    "sandhi",
                    "navami",
                    "dashami",
                )
            },
        ),
        (
            _("Shashti Puja Time"),
            {
                "fields": (
                    "shashtit",
                    "shashtite",
                )
            },
        ),
        (
            _("Saptami Puja Time"),
            {
                "fields": (
                    "saptamit",
                    "saptamite",
                )
            },
        ),
        (
            _("Ashtami Puja Time"),
            {
                "fields": (
                    "ashtamit",
                    "ashtamite",
                )
            },
        ),
        (
            _("Sandhi Puja Time"),
            {
                "fields": (
                    "sandhit",
                    "sandhite",
                )
            },
        ),
        (_("Maha Bhog Date and Time"), {
            "fields": ("mahabhog", "mahabhogdttime")
        }),
        (_("Navami Puja Time"), {
            "fields": ("navamit", "navamite")
        }),
        (
            _("Dashami Puja Time"),
            {
                "fields": (
                    "dashamit",
                    "dashamite",
                )
            },
        ),
    )


@admin.register(Videos)
class VideosAdmin(admin.ModelAdmin):
    list_display = (
        "streamingvideoheader",
        "streamingplatform",
        "yearmodel",
        "day",
        "live",
        "test",
    )
    list_filter = (
        ("yearmodel", RelatedDropdownFilter),
        ("day", ChoiceDropdownFilter),
        "live",
        "test",
    )
    search_fields = list_display + list_filter + ("streamingvideolink", )
    readonly_fields = ("video_posts", )
    list_per_page = 100

    fieldsets = (
        (_("Year"), {
            "fields": ("yearmodel", )
        }),
        (_("Day"), {
            "fields": ("day", )
        }),
        (_("Test"), {
            "fields": ("test", )
        }),
        (
            _("Streaming Video Data"),
            {
                "fields": (
                    "streamingvideoheader",
                    "streamingplatform",
                    "streamingvideodescription",
                )
            },
        ),
        (
            _("Streaming Video Links Data"),
            {
                "fields": (
                    "streamingvideolink",
                    "live",
                ) + readonly_fields
            },
        ),
    )

    # Custom Actions
    # live
    def make_videos_live(self, request, queryset):
        if len(queryset) > 1:
            self.message_user(request, "Please select only one video",
                              messages.ERROR)
        else:
            updated = queryset.update(live=True)

            self.message_user(
                request,
                ngettext(
                    "%d video was succesfully made live",
                    "%d videos were succesfully made live",
                    updated,
                ) % updated,
                messages.SUCCESS,
            )

    make_videos_live.short_description = "Make the selected videos go live"

    # offline
    def make_videos_offline(self, request, queryset):
        updated = queryset.update(live=False)
        self.message_user(
            request,
            ngettext(
                "%d video was succesfully made offline",
                "%d videos were succesfully made offline",
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    make_videos_offline.short_description = "Make the selected videos go offline"

    # maketest
    def maketest(self, request, queryset):
        updated = queryset.update(test=True)
        self.message_user(
            request,
            ngettext(
                "%d video was succesfully made as a test video",
                "%d videos were succesfully made as a test videos",
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    maketest.short_description = "Make the selected videos as a test video(s)"

    # removefromtest
    def removefromtest(self, request, queryset):
        updated = queryset.update(test=False)
        self.message_user(
            request,
            ngettext(
                "%d video was succesfully removed from test video",
                "%d videos were succesfully removed from test videos",
                updated,
            ) % updated,
            messages.SUCCESS,
        )

    removefromtest.short_description = (
        "Make the selected videos remove from test video(s)")

    # Registering the custom actions
    actions = [make_videos_live, make_videos_offline, maketest, removefromtest]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):

    def delete_admin_logs(self, request, queryset):
        querysetmsg = queryset.delete()

        self.message_user(
            request,
            ngettext(
                "%d log was successfully deleted.",
                "%d logs were successfully deleted.",
                len(queryset),
            ) % int(len(queryset)),
            messages.SUCCESS,
        )

    delete_admin_logs.short_description = (
        "Delete the selected ADMIN Logs without sticking")

    actions = [delete_admin_logs]


admin.site.unregister(Group)

admin.site.site_header = admin.site.site_title = "Shaw Durga Puja Live"
