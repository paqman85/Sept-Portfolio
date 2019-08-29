from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class SocialMediaSettings(BaseSetting):
    """Social Media Settings for our custom site."""

    facebook = models.URLField(blank=True, null=True, help_text="Facebook URL")
    twitter = models.URLField(blank=True, null=True, help_text="Twitter URL")
    youtube = models.URLField(blank=True, null=True, help_text="YouTube Channel URL")
    instagram = models.URLField(blank=True, null=True, help_text="Instgram URL")
    linkedin = models.URLField(blank=True, null=True, help_text="Linkedin URL")
    pinterest = models.URLField(blank=True, null=True, help_text="Pinterest URL")

    panels = [
        MultiFieldPanel([
            FieldPanel("facebook"),
            FieldPanel("twitter"),
            FieldPanel("youtube"),
            FieldPanel("instagram"),
            FieldPanel("linkedin"),
            FieldPanel("pinterest"),
        ], heading="Social Media Settings")
    ]