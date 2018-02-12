from django import template
from django.utils import translation
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(needs_autoescape=True)
def u(instance, title_attr='__str__', autoescape=None):
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    s = getattr(instance, title_attr)
    if callable(s):
        s = s()
    result = '<a href="%s">%s</a>' % (esc(instance.get_absolute_url()),
                                      esc(s))
    return mark_safe(result)


@register.filter
def bd(instance, field):
    lang = translation.get_language()[:2]
    return getattr(instance, field + "_" + lang)


@register.filter
def ut(instance, field='title'):
    lang = translation.get_language()[:2]
    attr = f"{field}_{lang}"
    return u(instance, attr)


@register.filter
def un(instance):
    return ut(instance, 'name')


@register.filter
def bdtitle(instance):
    lang = translation.get_language()[:2]
    return getattr(instance, "title_" + lang)
