from collections import defaultdict

from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from movies.models import Movie


class Person(models.Model):
    tid = models.IntegerField(unique=True)
    name_he = models.CharField(max_length=300, null=True, blank=True)
    name_en = models.CharField(max_length=300, null=True, blank=True)
    first_name_he = models.CharField(max_length=300, null=True, blank=True)
    first_name_en = models.CharField(max_length=300, null=True, blank=True)
    last_name_he = models.CharField(max_length=300, null=True, blank=True)
    last_name_en = models.CharField(max_length=300, null=True, blank=True)

    class Meta:
        verbose_name = _("person")
        verbose_name_plural = _("people")

    def __str__(self):
        return f"{self.first_name_en} {self.last_name_en}"

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


class Role(models.Model):
    tid = models.CharField(unique=True, max_length=300)
    title_en = models.CharField(max_length=300, null=True, blank=True)
    title_he = models.CharField(max_length=300, null=True, blank=True)
    appears_in_short_version = models.BooleanField(default=False)
    short_version_order = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title_he


class MovieRolePerson(models.Model):
    movie = models.ForeignKey(Movie, related_name='people')
    role = models.ForeignKey(Role, related_name='movie_people')
    person = models.ForeignKey(Person, related_name='movies')
