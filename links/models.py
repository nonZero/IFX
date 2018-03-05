from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import ugettext_lazy as _

from general.entities import ENTITY_CONTENT_TYPES
from ifx.base_models import Undeletable


class Language(object):
    HEBREW = 1
    ENGLISH = 2

    choices = (
        (HEBREW, _('Hebrew')),
        (ENGLISH, _('English')),
    )


class LinkTypeQuerySet(models.QuerySet):
    def get_by_natural_key(self, slug):
        return self.get(slug=slug)


class LinkType(Undeletable):
    title_he = models.CharField(_('Hebrew title'), max_length=300)
    title_en = models.CharField(_('English title'), max_length=300)
    slug = models.SlugField(_('slug'), unique=True)
    description_he = models.TextField(_('Hebrew description'), null=True,
                                      blank=True)
    description_en = models.TextField(_('English description'), null=True,
                                      blank=True)

    priority = models.IntegerField(_('priority'), default=100)

    title_required = models.BooleanField(_('title required'))
    for_movies = models.BooleanField(_('for movies'))
    for_people = models.BooleanField(_('for people'))

    wikidata_id = models.CharField(_('wikidata id'), max_length=50, null=True,
                                   blank=True)
    template = models.CharField(_('template'), max_length=500, null=True,
                                blank=True)

    objects = LinkTypeQuerySet.as_manager()

    def natural_key(self):
        return (self.slug,)

    class Meta:
        ordering = (
            'priority',
        )

    def __str__(self):
        return self.title_en


class Link(Undeletable):
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT,
                                     limit_choices_to=ENTITY_CONTENT_TYPES)
    object_id = models.PositiveIntegerField()
    entity = GenericForeignKey()

    type = models.ForeignKey(LinkType, related_name="%(class)ss",
                             on_delete=models.PROTECT, verbose_name=_('type'))
    value = models.CharField(_('value or URL'), max_length=400)
    title_he = models.CharField(_('Hebrew title'), max_length=300, null=True,
                                blank=True)
    title_en = models.CharField(_('English title'), max_length=300, null=True,
                                blank=True)
    notes_he = models.TextField(_('notes in Hebrew'), null=True, blank=True)
    notes_en = models.TextField(_('notes in English'), null=True, blank=True)
    language = models.IntegerField(_('language'), choices=Language.choices,
                                   null=True, blank=True)
    limit_to_language = models.BooleanField(_('limit to this language'),
                                            default=False)

    editing_comment = models.TextField(_('editing comment'), null=True,
                                       blank=True)

    created_at = models.DateTimeField(_('created at'), auto_now_add=True,
                                      db_index=True)

    FIELDS_TO_LOG = (
        'active',
        'content_type_id',
        'object_id',
        'type_id',
        'value',
        'title_he',
        'title_en',
        'notes_he',
        'notes_en',
        'language',
        'limit_to_language',
        'editing_comment',
        'created_at',
    )

    class Meta:
        ordering = (
            'type__priority',
            '-created_at',
        )

    def __str__(self):
        return f"{self.type}: {self.value}"

    def url(self):
        if self.type.template:
            return self.type.template.format(self.value)
        return self.value
