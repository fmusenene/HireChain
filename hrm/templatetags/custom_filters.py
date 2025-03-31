from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Fetches a dictionary item by key."""
    return dictionary.get(key, None)
