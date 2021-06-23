from django.db import models

from wagtail.core.models import Page

from wagtail.images.edit_handlers import ImageChooserPanel

from wagtail.api import APIField


class HomePage(Page):
    """Home page model."""

    max_count = 1

    hero_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel('hero_image'),
    ]

    api_fields = [
        APIField('hero_image')
    ]