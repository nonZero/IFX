from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

from movies.models import Movie


class Collection(models.Model):
    title = models.CharField(_("title"), max_length=300)

    class Meta:
        verbose_name = _("collection")
        verbose_name_plural = _("collections")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('curation:detail', args=(self.pk,))

    @property
    def title_he(self):
        # TODO: distinct titles
        return self.title

    @property
    def title_en(self):
        # TODO: distinct titles
        return self.title


class CollectionMovie(models.Model):
    collection = models.ForeignKey(Collection, related_name='movies',
                                   on_delete=models.PROTECT)
    movie = models.ForeignKey(Movie, related_name='collections',
                              on_delete=models.PROTECT)
    ordinal = models.IntegerField(default=100)

    def __str__(self):
        return 'Collection={}, Movie={}'.format(self.collection, self.movie)
