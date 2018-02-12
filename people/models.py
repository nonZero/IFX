from django.db import models
from django.urls import reverse

from movies.models import Movie


class Person(models.Model):
    tid = models.IntegerField(unique=True)
    name_he = models.CharField(max_length=300, null=True, blank=True)
    name_en = models.CharField(max_length=300, null=True, blank=True)
    first_name_he = models.CharField(max_length=300, null=True, blank=True)
    first_name_en = models.CharField(max_length=300, null=True, blank=True)
    last_name_he = models.CharField(max_length=300, null=True, blank=True)
    last_name_en = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name_en} {self.last_name_en}"

    def get_absolute_url(self):
        return reverse('people:detail', args=(self.pk,))



class Role(models.Model):
    tid = models.CharField(unique=True, max_length=300)
    title_en = models.CharField(max_length=300, null=True, blank=True)
    title_he = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title_he


class MovieRolePerson(models.Model):
    movie = models.ForeignKey(Movie, related_name='people')
    role = models.ForeignKey(Role, related_name='movie_people')
    person = models.ForeignKey(Person, related_name='movies')
