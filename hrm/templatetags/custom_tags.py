from django import template
from django.urls import resolve, reverse

register = template.Library()

@register.simple_tag(takes_context=True)
def is_active(context, url_name):
    request = context['request']
    current_url = request.path
    try:
        # Handle home page special case
        if url_name == 'home' and current_url == '/':
            return 'active'
        if url_name == 'hrm' and current_url == '/':
            return 'active'
        url = reverse(url_name)
        if current_url.startswith(url):
            return 'active'
    except:
        return ''
    return ''

@register.simple_tag(takes_context=True)
def is_menu_active(context, menu_urls):
    request = context['request']
    current_url = request.path
    try:
        for url_name in menu_urls.split(','):
            url_name = url_name.strip()
            # Handle home page special case
            if url_name == 'home' and current_url == '/':
                return 'show'
            if url_name == 'hrm' and current_url == '/':
                return 'show'
            url = reverse(url_name)
            if current_url.startswith(url):
                return 'show'
    except:
        return ''
    return '' 