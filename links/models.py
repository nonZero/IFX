from django.db import models
from django.utils.translation import ugettext_lazy as _

from ifx.base_models import Undeletable
from movies.models import Movie
from people.models import Person


class Language(object):
    HEBREW = 1
    ENGLISH = 2

    choices = (
        (HEBREW, _('Hebrew')),
        (ENGLISH, _('English')),
    )


class LinkType(Undeletable):
    title_he = models.CharField(max_length=300)
    title_en = models.CharField(max_length=300)
    slug = models.SlugField(unique=True)
    description_he = models.TextField(null=True, blank=True)
    description_en = models.TextField(null=True, blank=True)

    priority = models.IntegerField(default=100)

    title_required = models.BooleanField()
    for_movies = models.BooleanField()
    for_people = models.BooleanField()

    wikidata_id = models.CharField(max_length=50, null=True, blank=True)
    template = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title_en


class Link(Undeletable):
    type = models.ForeignKey(LinkType, related_name="%(class)ss")
    value = models.CharField(max_length=400)
    title_he = models.CharField(max_length=300, null=True, blank=True)
    title_en = models.CharField(max_length=300, null=True, blank=True)
    notes_he = models.TextField(null=True, blank=True)
    notes_en = models.TextField(null=True, blank=True)
    language = models.IntegerField(choices=Language.choices,
                                   null=True, blank=True)
    limit_to_language = models.BooleanField(default=False)

    editing_comment = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    FIELDS_TO_LOG = (
        'active',
        'parent_id',
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
        abstract = True

    def __str__(self):
        return f"{self.type}: {self.value}"


class MovieLink(Link):
    parent = models.ForeignKey(Movie, related_name='links')

    class Meta:
        unique_together = (
            ('parent', 'type', 'value'),
        )


class PersonLink(Link):
    parent = models.ForeignKey(Person, related_name='links')

    class Meta:
        unique_together = (
            ('parent', 'type', 'value'),
        )
