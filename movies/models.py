from collections import defaultdict

from django.db import models
from django.db.models import Count
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _


class Language(object):
    HEBREW = 'he'
    ENGLISH = 'en'

    choices = (
        (HEBREW, _('Hebrew')),
        (ENGLISH, _('English')),
    )


class Field(models.Model):
    fid = models.CharField(unique=True, max_length=300)
    title = models.CharField(_('title'), max_length=300)
    appears_in_short_version = models.BooleanField(
        _('appears in short version'), default=False)
    short_version_order = models.PositiveIntegerField(_('short version order'),
                                                      null=True, blank=True)

    class Meta:
        verbose_name = _("field")
        verbose_name_plural = _("fields")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movies:field_detail', args=(self.pk,))

    def get_tags(self):
        return Tag.objects.filter(movietagfield__field=self).annotate(
            count=Count('movietagfield')
        ).order_by('title')


class Tag(models.Model):
    tid = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    title_en = models.CharField(max_length=300, null=True, blank=True)
    title_he = models.CharField(max_length=300, null=True, blank=True)
    type_id = models.CharField(max_length=300, null=True, blank=True)
    lang = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('movies:tag_detail', args=(self.pk,))


class Movie(models.Model):
    bid = models.IntegerField(unique=True)
    year = models.IntegerField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    title_he = models.CharField(max_length=300, null=True, blank=True)
    title_en = models.CharField(max_length=300, null=True, blank=True)
    summary_he = models.TextField(null=True, blank=True)
    summary_en = models.TextField(null=True, blank=True)

    def __str__(self):
        return str('{}: "en:{}", "he:{}"'.format(self.id, self.title_en,
                                                 self.title_he))

    def get_absolute_url(self):
        return reverse('movies:detail', args=(self.pk,))

    def get_title(self):
        if self.title_he:
            return self.title_he
        elif self.title_en:
            return self.title_en
        return '<No Title>'

    def get_extra_data(self, short=False):
        mft = MovieTagField.objects.filter(movie=self.id)
        print(mft.count())
        if short:
            mft = mft.filter(field__appears_in_short_version=True).order_by(
                'field__short_version_order')
        fields = defaultdict(list)
        for item in mft:
            fields[item.field].append(item.tag)
        return list(fields.items())

    def get_short_data(self):
        return self.get_extra_data(short=True)

    def get_short_roles(self):
        return self.people.filter(
            role__appears_in_short_version=True).order_by(
            'role__short_version_order')


class MovieTagField(models.Model):
    movie = models.ForeignKey(Movie)
    field = models.ForeignKey(Field)
    tag = models.ForeignKey(Tag)

    def __str__(self):
        return 'Movie={}, Field={}, Tag={}'.format(
            self.movie, self.field, self.tag)
