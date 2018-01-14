from django import template
from django.utils.translation import get_language

register = template.Library()


@register.filter
def get_description(obj):
    lang = get_language()[:2]
    if lang == 'he':
        return obj.summary_he
    elif lang == 'en':
        return obj.summary_en
    return ''
