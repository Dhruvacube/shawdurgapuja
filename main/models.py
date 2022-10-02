import datetime
import urllib.parse
from typing import Union

from colorfield.fields import ColorField
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy as _

from discord_custom import *
from discord_custom.embeds import Embed


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year() + 10)(value)


dict_webhook = {
    "E": settings.HOMECOMING,
    "DI": settings.HOMECOMING,
    "T": settings.HOMECOMING,
    "C": settings.HOMECOMING,
    "P": settings.HOMECOMING,
    "S": settings.SHASHTI,
    "SA": settings.SAPTAMI,
    "A": settings.ASHTAMI,
    "SAN": settings.ASHTAMI,
    "N": settings.NAVAMI,
    "D": settings.DASHAMI,
}

dict_colors = {
    "E": Color.blurple(),
    "DI": Color.blurple(),
    "T": Color.blurple(),
    "C": Color.blurple(),
    "P": Color.orange(),
    "S": Color.yellow(),
    "SA": Color.default(),
    "A": Color.red(),
    "SAN": Color.dark_theme(),
    "N": Color.dark_blue(),
    "D": Color.gold(),
}

dict_roles = {
    "E": 922006581334405187,
    "DI": 922006581334405187,
    "T": 922006581334405187,
    "C": 922006581334405187,
    "P": 922006581334405187,
    "S": 922006581334405186,
    "SA": 922006581334405185,
    "A": 922006581334405184,
    "SAN": 922006581334405184,
    "N": 922006581334405183,
    "D": 922006581334405182,
}

dict_days = {
    "E": "Ekum",
    "DI": "Dvitia",
    "T": "Tritiya",
    "C": "Maha Chathurti",
    "P": "Maha Panchami",
    "S": "Maha Shashti",
    "SA": "Maha Saptami",
    "A": "Maha Ashtami",
    "SAN": "Sandhi Puja",
    "N": "Maha Navami",
    "D": "Maha Dashami",
}

dict_channel_id = {
    "E": 923915122852921404,
    "DI": 923915122852921404,
    "T": 923915122852921404,
    "C": 923915122852921404,
    "P": 923915122852921404,
    "S": 923915169749434408,
    "SA": 923915500596129822,
    "A": 923915574520717322,
    "SAN": 923915574520717322,
    "N": 923915679722274847,
    "D": 923915707362713670,
}


class Year(models.Model):
    """
    Model to store the Year of Durga Puja live links and its correspondence
    """

    year = models.IntegerField(
        _("Year"),
        unique=True,
        validators=[MinValueValidator(2003), max_value_current_year],
    )

    colourback = ColorField(_("colourback"),
                            default="#496D89",
                            blank=True,
                            null=True)
    colourtext = ColorField(_("colourtext"),
                            default="#FFF00C",
                            blank=True,
                            null=True)
    yeardesc = models.TextField(_("About the year"), blank=True, null=True)

    maacomevid = models.BooleanField(
        _("Will there be any video for the Maa Durga coming to home"),
        default=True,
        help_text="Check this checkbox if there will be any video of the Maa coming to home",
    )

    shashti = models.DateField(_("Date of Shashti Puja"),
                               blank=True,
                               null=True)
    saptami = models.DateField(_("Date of Saptami Puja"),
                               blank=True,
                               null=True)
    ashtami = models.DateField(_("Date of Ashtami Puja"),
                               blank=True,
                               null=True)
    sandhi = models.DateField(_("Date of Sandhi Puja"), blank=True, null=True)
    navami = models.DateField(_("Date of Navami Puja"), blank=True, null=True)
    dashami = models.DateField(_("Date of Dashami Puja"),
                               blank=True,
                               null=True)

    # Puja Timings
    shashtit = models.TimeField(_("Start Time of Shashti Puja"),
                                blank=True,
                                null=True)
    shashtite = models.TimeField(_("End Time of Shashti Puja"),
                                 blank=True,
                                 null=True)

    saptamit = models.TimeField(_("Start Time of Saptami Puja"),
                                blank=True,
                                null=True)
    saptamite = models.TimeField(_("End Time of Saptami Puja"),
                                 blank=True,
                                 null=True)

    ashtamit = models.TimeField(_("Start Time of Ashtami Puja"),
                                blank=True,
                                null=True)
    ashtamite = models.TimeField(_("End Time of Ashtami Puja"),
                                 blank=True,
                                 null=True)
    mahabhog = models.BooleanField(
        _("Maha Bhog is there ?"),
        help_text=_("Click only when Maha Bhog is organised."),
        default=False,
    )
    mahabhogdttime = models.DateTimeField(
        _("Maha Bhog Date and Time"),
        help_text=_('Fill this only when "Maha Bhog checkbox" is clicked.'),
        null=True,
        blank=True,
    )

    sandhit = models.TimeField(_("Start Time of Sandhi Puja"),
                               blank=True,
                               null=True)
    sandhite = models.TimeField(_("End Time of Sandhi Puja"),
                                blank=True,
                                null=True)

    navamit = models.TimeField(_("Start Time of Navami Puja"),
                               blank=True,
                               null=True)
    navamite = models.TimeField(_("End Time of Navami Puja"),
                                blank=True,
                                null=True)

    dashamit = models.TimeField(_("Start Time of Dashami Puja"),
                                blank=True,
                                null=True)
    dashamite = models.TimeField(_("End Time of Dashami Puja"),
                                 blank=True,
                                 null=True)

    class Meta:
        ordering = ("-year", )

    def __str__(self):
        return str(self.year)

    def view_puja_dates_and_time(self):
        """A button to view the pdf puja schedule file"""
        return mark_safe(
            f'<a href="pdf/{self.pujadatetime.url}" onclick="return showAddAnotherPopup(this)" class="submit-row">Click Here</a>'
        )


def get_default_year():
    from datetime import datetime

    return Year.objects.get_or_create(year=int(datetime.now().strftime("%Y")))


def get_video_id(video_url: str) -> Union[str, None]:
    if "youtube.com/watch?v=" in video_url:
        return urllib.parse.parse_qs(
            urllib.parse.urlparse(video_url).query)["v"][0]
    elif "youtu.be/" in video_url:
        return video_url.lstrip("/").split("/")[-1]


def validate_url(value):
    if ("youtube.com", "youtu.be", "youtube", "youtu") in value:
        raise ValidationError(_("Please put a Facebook Url !"), )
    if ("facebook.com", "fb.watch") in value:
        raise ValidationError(_("Please put a YouTube Url !"), )


class Videos(models.Model):
    """
    Stores a single Video entry, related to :model:`main.Year`
    according the day of uploading (Maha Shashti, Maha Saptami, Maha Ashtami, Maha Navami, Maha Dashami)
    """

    yearmodel = models.ForeignKey(
        Year,
        verbose_name=_("Year"),
        null=True,
        default=get_default_year,
        on_delete=models.SET_NULL,
    )
    day = models.CharField(
        _("Day of Uploading"),
        null=True,
        blank=True,
        choices=(
            ("E", "Ekum"),
            ("DI", "Dvitia"),
            ("T", "Tritiya"),
            ("C", "Maha Chathurti"),
            ("P", "Maha Panchami"),
            ("S", "Maha Shashti"),
            ("SA", "Maha Saptami"),
            ("A", "Maha Ashtami"),
            ("SAN", "Sandhi Puja"),
            ("N", "Maha Navami"),
            ("D", "Maha Dashami"),
        ),
        max_length=50,
        default="S",
    )

    test = models.BooleanField(
        _("Test"),
        default=False,
        help_text=_("Check this only when you are testing the webhook"),
    )

    streamingplatform = models.CharField(
        _("Streaming Platform"),
        null=True,
        blank=True,
        choices=(("F", "Facebook"), ("Y", "YouTube")),
        max_length=10,
        default="F",
    )
    streamingvideoheader = models.CharField(_("Live Streaming Video Header"),
                                            null=True,
                                            blank=True,
                                            max_length=600)

    streamingvideolink = models.URLField(_("Live Video Link"),
                                         validators=[validate_url])
    live = models.BooleanField(
        _("Live Video"),
        help_text=_("Check this only if the video is live"),
        default=True,
    )
    embeedlink = models.URLField(_("Embed Link of Posts or Video"),
                                 null=True,
                                 blank=True)
    streamingvideodescription = models.TextField(
        _("Streaming Video Short Description"),
        help_text="This is optional",
        null=True,
        blank=True,
    )

    def __str__(self):
        try:
            aname = (self.streamingvideoheader + " " + str(
                Year.objects.values("year").filter(
                    id=self.yearmodel.id).get()["year"]))
        except:
            aname = ("Deleted Year" + " " + self.streamingvideoheader + " " +
                     f"({self.day})")
        return aname

    def get_absolute_url(self):
        return reverse("Videos", args=[self.yearmodel.year, self.day])

    def video_posts(self):
        """This is method to generate the facebook video in an iframe"""
        if self.embeedlink:
            return mark_safe(
                f'<iframe loading="lazy" src="{self.embeedlink}"  width="734" height="504" style="border:none;overflow:hidden" scrolling="no" frameborder="0" allowfullscreen="true" allow="autoplay; clipboard-write; encrypted-media; picture-in-picture; web-share" allowFullScreen="true"></iframe>'
            )
        return mark_safe("<h4>No FB/ Youtube Video for now</h4>")

    def save(self, *args, **kwargs):
        self.streamingvideolink = self.streamingvideolink.rstrip("/")
        if self.streamingplatform == "F":
            self.embeedlink = f"https://www.facebook.com/plugins/video.php?height=504&href={urllib.parse.quote_plus(self.streamingvideolink)}&show_text=false&width=734&t=0"
        else:
            self.embeedlink = ("https://www.youtube.com/embed/" +
                               get_video_id(self.streamingvideolink).strip())

        if self.live:
            Videos.objects.update(live=False)
            self.live = self.live

        if not Videos.objects.filter(id=self.id).exists():
            webhook = dict_webhook[
                self.day] if not self.test else settings.TEST
            if webhook.lower().startswith("https://discord.com/api"):
                webhook = webhook[len("https://discord.com/api"):]
            embed = Embed(
                title=self.streamingvideoheader.capitalize(),
                color=dict_colors[self.day]
                if not self.test else Color.default(),
                url=f'https://shawdurgapuja.herokuapp.com/{reverse("Videos",args=[self.yearmodel.year, self.day])}#live',
            )
            description = f"```A new puja video for the year {self.yearmodel.year} has gone live```"
            description1 = f"> ``See the video`` : [Click Here]({self.streamingvideolink}) <a:liveyellow:853661056592117792>"
            description2 = f'> ``See the video in the site`` : [Click Here](https://shawdurgapuja.herokuapp.com/{reverse("Videos",args=[self.yearmodel.year, self.day])}#live)'
            embed.set_author(
                name=dict_days[self.day],
                icon_url="https://cdn.discordapp.com/avatars/853644680486191106/ee39d19c48c4ff53bb4d75e667ff2df3.png",
            )
            embed.description = f"{description}\n\n{description1}\n{description2}"
            discord_api_req(
                path=webhook,
                method="post",
                data={
                    "content":
                    f"<@&{dict_roles[self.day]}>",
                    "embeds": [embed.to_dict()],
                    "allowed_mentions":
                    AllowedMentions(everyone=True, roles=True,
                                    users=True).to_dict(),
                },
            )
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Videos"
