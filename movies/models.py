from django.db import models
from django.utils.translation import ugettext_lazy as _


class Languages(object):
    choices = (
        ('he', _('Hebrew')),
        ('en', _('English')),
    )


class Field(models.Model):
    fid = models.CharField(unique=True, max_length=300)
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Tag(models.Model):
    tid = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    type_id = models.CharField(max_length=300, null=True, blank=True)
    lang = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title


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

    def get_title(self):
        if self.title_he:
            return self.title_he
        elif self.title_en:
            return self.title_en
        return '<No Title>'

    def get_extra_data(self):
        mft = MovieTagField.objects.filter(movie=self.id)
        fields = {}
        for item in mft:
            if item.field.title in fields:
                fields[item.field.title].append(item.tag.title)
            else:
                fields[item.field.title] = [(item.tag.title)]

        return fields


class MovieTagField(models.Model):
    movie = models.ForeignKey(Movie)
    field = models.ForeignKey(Field)
    tag = models.ForeignKey(Tag)

    def __str__(self):
        return 'Movie={}, Field={}, Tag={}'.format(self.movie, self.field,
                                                   self.tag)


class Collection(models.Model):
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title

    def get_items(self):
        return CollectionMovie.objects.filter(collection=self.id)


class CollectionMovie(models.Model):
    collection = models.ForeignKey(Collection)
    movie = models.ForeignKey(Movie)

    def __str__(self):
        return 'Collection={}, Movie={}'.format(self.collection, self.movie)


class Person(models.Model):
    tid = models.IntegerField(unique=True)
    name_he = models.CharField(max_length=300, null=True, blank=True)
    name_en = models.CharField(max_length=300, null=True, blank=True)
    first_name_he = models.CharField(max_length=300, null=True, blank=True)
    first_name_en = models.CharField(max_length=300, null=True, blank=True)
    last_name_he = models.CharField(max_length=300, null=True, blank=True)
    last_name_en = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        if self.name_en:
            return self.name_en
        elif self.first_name_en and self.last_name_en:
            return self.first_name_en + " " + self.last_name_en


class Role(models.Model):
     tid = models.CharField(unique=True, max_length=300)
     title_en = models.CharField(max_length=300, null=True, blank=True)
     title_he = models.CharField(max_length=300, null=True, blank=True)
 

class MovieRolePerson(models.Model):
     movie = models.ForeignKey(Movie, related_name='people')
     role = models.ForeignKey(Role, related_name='movie_people')
     person = models.ForeignKey(Person, related_name='movies')