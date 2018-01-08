from django import template
from django.utils.translation import get_language

register = template.Library()

@register.filter
def get_description(obj):
    lang = get_language()[:2]
    print(lang)
    lang = 'HEB'
    res = obj.description.filter(lang=lang)
    if res:
        return res[0].summery
    return ''