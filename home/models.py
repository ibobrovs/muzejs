from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail import blocks
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock

# Страница-список новостей
class AktualitatesPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]

    subpage_types = ['home.AktualitateDetailPage']

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