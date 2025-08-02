from django import template
from wagtail.models import Page

register = template.Library()

@register.inclusion_tag('home/includes/menu_items.html', takes_context=True)
def main_menu(context, calling_page=None):
    request = context['request']

    if calling_page:
        parent = calling_page.get_parent()
        menu_items = parent.get_children().live().in_menu()
    else:
        menu_items = []

    return {
        'menu_items': menu_items,
        'request': request
    }
