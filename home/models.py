from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock


class HomePage(Page):
    intro = models.CharField(max_length=255, blank=True)

    banner = StreamField([
        ('banner', blocks.StructBlock([
            ('title', blocks.CharBlock(required=True)),
            ('subtitle', blocks.TextBlock(required=False)),
            ('background_image', ImageChooserBlock(required=False)),
        ])),
    ], use_json_field=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('banner'),
    ]
    
# Страница-список новостей
class AktualitatesPage(Page):
    body = StreamField([
        ("heading", blocks.CharBlock(classname="full title")),
        ("paragraph", blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("body")
    ]

# Страница одной новости
class AktualitateDetailPage(Page):
    date = models.DateField("Publicēšanas datums")
    body = StreamField([
        ("heading", blocks.CharBlock(classname="full title")),
        ("paragraph", blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("body"),
    ]

    parent_page_types = ['home.AktualitatesPage']


class EkspozicijasPage(Page):
    intro = RichTextField(blank=True, verbose_name="Ievads")
    body = StreamField([
        ("virsraksts", blocks.CharBlock(classname="full title", label="Virsraksts")),
        ("teksts", blocks.RichTextBlock(label="Teksts")),
        ("attels", ImageChooserBlock(label="Attēls")),
    ], use_json_field=True, verbose_name="Saturs")

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]


class GalerijasPage(Page):
    gallery = StreamField([
        ("image", blocks.StructBlock([
            ("title", blocks.CharBlock(required=False)),
            ("image", ImageChooserBlock(required=True)),
        ])),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("gallery"),
    ]