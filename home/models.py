from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.images.blocks import ImageChooserBlock
from wagtail import blocks
from wagtail.admin.panels import FieldPanel


# -- Главная страница
class HomePage(Page):
    intro = models.CharField(max_length=255, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]


# -- О музее
class ParMuzejuPage(Page):
    body = StreamField([
        ("heading", blocks.CharBlock(classname="full title")),
        ("paragraph", blocks.RichTextBlock()),
        ("image", ImageChooserBlock()),
    ], use_json_field=True)

    content_panels = Page.content_panels + [
        FieldPanel("body")
    ]


# -- Контакты
class KontaktiPage(Page):
    address = models.TextField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    map_embed = models.TextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("address"),
        FieldPanel("phone"),
        FieldPanel("email"),
        FieldPanel("map_embed"),
    ]


# -- Список событий
class EventsPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]


# -- Отдельное событие
class EventDetailPage(Page):
    date = models.DateField()
    description = RichTextField(blank=True)
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("description"),
        FieldPanel("image"),
    ]

    parent_page_types = ['home.EventsPage']


# -- Visit info (для посетителей)
class VisitPage(Page):
    info = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("info"),
    ]
