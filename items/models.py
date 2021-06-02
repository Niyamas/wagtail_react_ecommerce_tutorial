from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL
from django.db.models.fields.files import ImageField
from django.utils.text import slugify 

from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    InlinePanel,
)
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.api import APIField
from wagtail.snippets.models import register_snippet

class ItemListingPage(Page):
    """Item listing page that houses the categories and each item page."""

    parent_page_types = ['home.HomePage']
    subpage_types = ['items.ItemDetailPage']
    max_count = 1

class ItemDetailPage(Page):
    """Individual item model."""

    parent_page_types = ['items.ItemListingPage']
    subpage_types = []

    user = models.ForeignKey(
        User,
        blank=True,
        null=True,
        on_delete=models.SET_NULL       # When deleting user, set this value to null

    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        help_text='Sample help text. Change later yes',
        on_delete=models.SET_NULL
    )
    category = models.ForeignKey(
        'items.ItemCategory',
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    brand = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    description = RichTextField(
        features=['bold', 'italic'],
        max_length=2000,
        blank=False,
        null=True
    )
    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True
    )
    quantity_in_stock = models.IntegerField(
        default=0,
        blank=False,
        null=True,
    )
    rating = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True
    )
    quantity_reviews = models.IntegerField(
        default=0,
        blank=False,
        null=True,
    )

    content_panels = Page.content_panels + [
        FieldPanel('user'),
        MultiFieldPanel(
            [
                ImageChooserPanel('image'),
                FieldPanel('category'),
                FieldPanel('brand'),
                FieldPanel('description'),
                FieldPanel('price'),
                FieldPanel('quantity_in_stock'),
            ],
            heading='Item Information'
        ),
        MultiFieldPanel(
            [
                FieldPanel('rating'),
                FieldPanel('quantity_reviews')
            ],
            heading='Item Reviews'
        )
    ]

    # Export fields over the API
    api_fields = [
        APIField('user'),
        APIField('image'),
        APIField('brand'),
        APIField('description'),
        APIField('price'),
        APIField('quantity_in_stock'),
        APIField('rating'),
        APIField('quantity_reviews'),
    ]


@register_snippet
class ItemCategory(models.Model):
    """Adds an item category section in Snippets. Can be linked with item detail pages."""

    name = models.CharField(
        max_length=100
    )
    slug = models.SlugField(
        unique=True,
        blank=True,
        null=True
    )

    panels = [
        FieldPanel('name'),
        FieldPanel('slug')
    ]

    class Meta:
        verbose_name = 'Item Category'
        verbose_name_plural = 'Item Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(ItemCategory, self).save(*args, **kwargs)
        self.slug = slugify(self.name, allow_unicode=True)
        return super(ItemCategory, self).save(*args, **kwargs)




