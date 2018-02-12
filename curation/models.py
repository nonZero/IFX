from django.db import models

from movies.models import Movie


class Collection(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class CollectionMovie(models.Model):
    collection = models.ForeignKey(Collection, related_name='movies')
    movie = models.ForeignKey(Movie, related_name='collections')
    ordinal = models.IntegerField(default=100)

    def __str__(self):
        return 'Collection={}, Movie={}'.format(self.collection, self.movie)
