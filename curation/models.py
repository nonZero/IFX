from django.db import models
from django.urls import reverse

from movies.models import Movie


class Collection(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('curation:detail', args=(self.pk,))


class CollectionMovie(models.Model):
    collection = models.ForeignKey(Collection, related_name='movies')
    movie = models.ForeignKey(Movie, related_name='collections')
    ordinal = models.IntegerField(default=100)

    def __str__(self):
        return 'Collection={}, Movie={}'.format(self.collection, self.movie)
