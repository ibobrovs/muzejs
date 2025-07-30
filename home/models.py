from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField, RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


# ----------------------------- #
# Главная
# ----------------------------- #
class HomePage(Page):
    template = "home/home_page.html"

    intro = models.CharField("Ievads", max_length=255, blank=True)

    # Разрешаем создавать только нужные разделы под корнем
    subpage_types = [
        "AktualitatesIndexPage",
        "EkspozicijasPage",
        "IzstadesIndexPage",
        "PetniecibaIndexPage",
        "KrajumsIndexPage",
        "GalerijasPage",
        "PakalpojumiPage",
        "ParMuzejuPage",
        "SaitesPage",
        "KontaktiPage",
    ]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]


# ----------------------------- #
# AKTUALITĀTES (список и детальная)
# ----------------------------- #
class AktualitatesIndexPage(Page):
    template = "home/aktualitates_page.html"

    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock(features=["h2", "h3", "bold", "italic", "link", "ol", "ul"])),
        ],
        use_json_field=True,
        blank=True,
    )

    parent_page_types = ["HomePage"]
    subpage_types = ["AktualitatePage"]

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class AktualitatePage(Page):
    template = "home/aktualitate_detail_page.html"

    date = models.DateField("Publicēšanas datums")
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock(features=["h2", "h3", "bold", "italic", "link", "ol", "ul"])),
            ("image", ImageChooserBlock()),
        ],
        use_json_field=True,
    )

    parent_page_types = ["AktualitatesIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("body"),
    ]


# ----------------------------- #
# EKPSOZĪCIJAS (одна страница с гибким контентом)
# ----------------------------- #
class EkspozicijasPage(Page):
    template = "home/ekspozicijas_page.html"

    intro = RichTextField(blank=True, verbose_name="Ievads")
    body = StreamField(
        [
            ("title", blocks.CharBlock(label="Virsraksts")),
            ("text", blocks.RichTextBlock(label="Teksts")),
            ("image", ImageChooserBlock(label="Attēls")),
            ("gallery", blocks.ListBlock(ImageChooserBlock(label="Attēls"), label="Galerija", help_text="Attēlu saraksts")),
        ],
        use_json_field=True,
        verbose_name="Saturs",
        blank=True,
    )

    parent_page_types = ["HomePage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
        FieldPanel("body"),
    ]


# ----------------------------- #
# IZSTĀDES (временные выставки: список + детальная)
# ----------------------------- #
class IzstadesIndexPage(Page):
    template = "home/izstades_page.html"

    intro = RichTextField(blank=True, verbose_name="Ievads")

    parent_page_types = ["HomePage"]
    subpage_types = ["IzstadePage"]

    content_panels = Page.content_panels + [
        FieldPanel("intro"),
    ]


class IzstadePage(Page):
    template = "home/izstade_detail_page.html"

    date_from = models.DateField("Sākuma datums")
    date_to = models.DateField("Beigu datums", blank=True, null=True)
    location = models.CharField("Vieta", max_length=255, blank=True)
    body = StreamField(
        [
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("gallery", blocks.ListBlock(ImageChooserBlock(label="Attēls"), label="Galerija")),
        ],
        use_json_field=True,
        blank=True,
    )

    parent_page_types = ["IzstadesIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("date_from"),
        FieldPanel("date_to"),
        FieldPanel("location"),
        FieldPanel("body"),
    ]


# ----------------------------- #
# PĒTNIECĪBA (исследования: список + статья)
# ----------------------------- #
class PetniecibaIndexPage(Page):
    template = "home/petnieciba_page.html"

    parent_page_types = ["HomePage"]
    subpage_types = ["PetniecibaArticlePage"]

    content_panels = Page.content_panels


class PetniecibaArticlePage(Page):
    template = "home/petnieciba_article_page.html"

    authors = models.CharField("Autori", max_length=255, blank=True)
    date = models.DateField("Datums")
    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
            ("quote", blocks.BlockQuoteBlock()),
        ],
        use_json_field=True,
    )

    parent_page_types = ["PetniecibaIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("authors"),
        FieldPanel("date"),
        FieldPanel("body"),
    ]


# ----------------------------- #
# KRĀJUMS (коллекция: список + элемент)
# ----------------------------- #
class KrajumsIndexPage(Page):
    template = "home/krajums_page.html"

    parent_page_types = ["HomePage"]
    subpage_types = ["KrajumsItemPage"]

    content_panels = Page.content_panels


class KrajumsItemPage(Page):
    template = "home/krajums_item_page.html"

    inventory_no = models.CharField("Inventāra numurs", max_length=100, blank=True)
    period = models.CharField("Periods", max_length=100, blank=True)
    description = RichTextField("Apraksts", blank=True)
    images = StreamField(
        [("image", ImageChooserBlock())],
        use_json_field=True,
        blank=True,
        verbose_name="Attēli",
    )

    parent_page_types = ["KrajumsIndexPage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("inventory_no"),
        FieldPanel("period"),
        FieldPanel("description"),
        FieldPanel("images"),
    ]


# ----------------------------- #
# GALERIJAS (фото-галерея)
# ----------------------------- #
class GalerijasPage(Page):
    template = "home/galerijas_page.html"

    gallery = StreamField(
        [
            ("image", blocks.StructBlock([
                ("title", blocks.CharBlock(required=False)),
                ("image", ImageChooserBlock(required=True)),
            ])),
        ],
        use_json_field=True,
        blank=True,
    )

    parent_page_types = ["HomePage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("gallery"),
    ]


# ----------------------------- #
# PAKALPOJUMI (услуги и прайс)
# ----------------------------- #
class PakalpojumiPage(Page):
    template = "home/pakalpojumi_page.html"

    services = StreamField(
        [
            ("service", blocks.StructBlock([
                ("title", blocks.CharBlock(label="Nosaukums")),
                ("price", blocks.CharBlock(label="Cena", required=False)),
                ("desc", blocks.RichTextBlock(label="Apraksts", required=False)),
            ])),
        ],
        use_json_field=True,
        blank=True,
        verbose_name="Pakalpojumi",
    )

    parent_page_types = ["HomePage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("services"),
    ]


# ----------------------------- #
# PAR MUZEJU (о музее)
# ----------------------------- #
class ParMuzejuPage(Page):
    template = "home/parm_s_page.html"

    body = StreamField(
        [
            ("heading", blocks.CharBlock(classname="full title")),
            ("paragraph", blocks.RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        use_json_field=True,
        blank=True,
    )

    parent_page_types = ["HomePage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


# ----------------------------- #
# SAITES (полезные ссылки)
# ----------------------------- #
class SaitesPage(Page):
    template = "home/saites_page.html"

    links = StreamField(
        [
            ("link", blocks.StructBlock([
                ("title", blocks.CharBlock(label="Nosaukums")),
                ("url", blocks.URLBlock(label="Saite")),
                ("desc", blocks.TextBlock(label="Apraksts", required=False)),
                ("newtab", blocks.BooleanBlock(label="Atvērt jaunā cilnē", required=False)),
            ])),
        ],
        use_json_field=True,
        blank=True,
    )

    parent_page_types = ["HomePage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("links"),
    ]


# ----------------------------- #
# KONTAKTI
# ----------------------------- #
class KontaktiPage(Page):
    template = "home/kontakti_page.html"

    address = models.TextField("Adrese", blank=True)
    phone = models.CharField("Tālrunis", max_length=50, blank=True)
    email = models.EmailField("E-pasts", blank=True)
    map_embed = models.TextField("Kartes ieliktnis (iframe)", blank=True)

    parent_page_types = ["HomePage"]
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("address"),
        FieldPanel("phone"),
        FieldPanel("email"),
        FieldPanel("map_embed"),
    ]
