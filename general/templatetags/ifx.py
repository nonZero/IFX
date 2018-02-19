from urllib.parse import urlencode

from django import template
from django.utils import translation
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag("_pagination.html", takes_context=True)
def pagination(context, page_obj):
    return {
        'request': context['request'],
        'page_obj': page_obj,
    }


@register.simple_tag(takes_context=True)
def qs(context, **kwargs):
    items = {**context.request.GET.dict(), **kwargs}
    return urlencode(items)


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


@register.filter
def bdorder(qs):
    lang = translation.get_language()[:2]
    return qs.order_by("title_" + lang)


@register.filter
def duration(n: int):
    return "{:01.0f}:{:02.0f}".format(*divmod(n, 60))
