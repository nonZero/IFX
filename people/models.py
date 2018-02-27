from collections import defaultdict

from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from enrich.wikidata import HUMAN
from ifx.base_models import Undeletable, WikiDataEntity
from movies.models import Movie


class Person(Undeletable, WikiDataEntity):
    ENTITY_CODE = 'person'
    WIKIDATA_CLASSIFIER_PID = HUMAN

    name_he = models.CharField(max_length=300, null=True, blank=True,
                               db_index=True)
    name_en = models.CharField(max_length=300, null=True, blank=True,
                               db_index=True)
    first_name_he = models.CharField(max_length=300, null=True, blank=True,
                                     db_index=True)
    first_name_en = models.CharField(max_length=300, null=True, blank=True,
                                     db_index=True)
    last_name_he = models.CharField(max_length=300, null=True, blank=True,
                                    db_index=True)
    last_name_en = models.CharField(max_length=300, null=True, blank=True,
                                    db_index=True)
    idea_tid = models.IntegerField(unique=True, null=True, blank=True)
    idea_modified = models.BooleanField(default=False)

    links = GenericRelation('links.Link')
    suggestions = GenericRelation('enrich.Suggestion')

    FIELDS_TO_LOG = (
        'name_he',
        'name_en',
        'first_name_he',
        'first_name_en',
        'last_name_he',
        'last_name_en',
        'idea_tid',
        'idea_modified',
        'wikidata_status',
        'wikidata_id',
    )

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def __str__(self):
        return str(self.name_en or self.name_he)

    def get_absolute_url(self):
        return reverse('people:detail', args=(self.pk,))

    def distinct_roles(self):
        return self.movies.distinct('role')

    def movies_flat(self):
        movies = defaultdict(set)
        for mrp in self.movies.order_by('-movie__year'):
            movies[mrp.movie].add(mrp.role)

        for m, roles in movies.items():
            m.roles = roles
            yield m

    @property
    def title_he(self):
        return self.name_he

    @property
    def title_en(self):
        return self.name_en


class Role(Undeletable, WikiDataEntity):
    title_en = models.CharField(max_length=300, null=True, blank=True)
    title_he = models.CharField(max_length=300, null=True, blank=True)
    priority = models.PositiveIntegerField(default=100)
    appears_in_short_version = models.BooleanField(default=False)
    short_version_order = models.PositiveIntegerField(null=True, blank=True)
    idea_tid = models.CharField(unique=True, max_length=300, null=True,
                                blank=True)
    idea_modified = models.BooleanField(default=False)

    FIELDS_TO_LOG = (
        'title_en',
        'title_he',
        'priority',
        'appears_in_short_version',
        'short_version_order',
        'idea_tid',
        'idea_modified',
    )

    def __str__(self):
        return self.title_en or self.title_he or "???"


class MovieRolePerson(Undeletable):
    movie = models.ForeignKey(Movie, related_name='people',
                              on_delete=models.PROTECT)
    role = models.ForeignKey(Role, related_name='movie_people',
                             on_delete=models.PROTECT)
    person = models.ForeignKey(Person, related_name='movies',
                               on_delete=models.PROTECT)
    priority = models.PositiveIntegerField(default=100)
    note = models.CharField(max_length=250, null=True, blank=True)
    idea_uid = models.IntegerField(null=True, blank=True, unique=True)
    idea_modified = models.BooleanField(default=False)

    FIELDS_TO_LOG = (
        'movie_id',
        'role_id',
        'person_id',
        'priority',
        'note',
        'idea_uid',
        'idea_modified',
    )

    class Meta:
        unique_together = (
            ('movie', 'role', 'person'),
        )
