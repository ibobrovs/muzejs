from django import template
from wagtail.models import Page

register = template.Library()

@register.inclusion_tag('home/includes/header.html', takes_context=True)
def main_menu(context):
    root = Page.get_first_root_node()
    menu_items = root.get_children().live().in_menu()
    return {
        'menu_items': menu_items,
        'request': context['request'],
    }
