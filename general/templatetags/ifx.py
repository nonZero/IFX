from urllib.parse import urlencode

from django import template
from django.utils import translation
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _

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


FLIP = {'en': 'he', 'he': 'en'}


@register.filter
def bdtitle_plus(instance):
    lang = translation.get_language()[:2]
    title = getattr(instance, "title_" + lang)
    if not title:
        title = getattr(instance, "title_" + FLIP[lang])
    return title

@register.filter
def ut_plus(instance, field='title'):
    lang = translation.get_language()[:2]
    attr = f"{field}_{lang}"
    if not getattr(instance, attr):
        attr = f"{field}_{FLIP[lang]}"
    return u(instance, attr)



@register.filter
def bdorder(qs):
    lang = translation.get_language()[:2]
    return qs.order_by("title_" + lang)


@register.filter
def duration(n: int):
    return "{:01.0f}:{:02.0f}".format(*divmod(n, 60))


@register.inclusion_tag('enrich/_search_link.html')
def google_search(q):
    return {
        'title': _('Google search'),
        'url': 'https://www.google.com/search?q=',
        'class': 'fab fa-google',
        'q': q,
    }


@register.inclusion_tag('enrich/_search_link.html')
def imdb_search(q):
    return {
        'title': _('IMDB search'),
        'url': 'http://www.imdb.com/find?s=all&q=',
        'class': 'fab fa-imdb',
        'q': q,
    }


@register.inclusion_tag('enrich/_search_link.html')
def wikidata_search(q):
    return {
        'title': _('WikiData search'),
        'url': 'https://www.wikidata.org/w/index.php?search=',
        'class': 'fa fa-barcode',
        'q': q,
    }


@register.inclusion_tag('enrich/_search_link.html')
def wikipedia_search(lang, q):
    return {
        'title': _('Wikipedia search'),
        'url': f'https://{lang}.wikipedia.org/w/index.php?search=',
        'class': 'fa fa-wikipedia',
        'q': q,
    }


@register.inclusion_tag('enrich/_search_links.html')
def search_links(q, lang='he'):
    return {
        'lang': lang,
        'q': q,
    }


@register.filter
def tolist(x):
    return list(x)
