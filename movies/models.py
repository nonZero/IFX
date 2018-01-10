from django.db import models
from django.utils.translation import ugettext_lazy as _


class Tag(models.Model):
    tid = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    type_1 = models.CharField(max_length=300, null=True, blank=True)

    def __str__(self):
        return self.title


class Field(models.Model):
    fid = models.CharField(unique=True, max_length=300)
    title = models.CharField(max_length=300)
    
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
        return str('{}: "en:{}", "he:{}"'.format(self.id, self.title_en, self.title_he))
    
    def get_title(self):
        if self.title_he:
            return self.title_he
        elif self.title_en:
            return self.title_en
        return '<No Title>'

    def get_extra_data(self):
        mft = Movie_Tag_Field.objects.filter(movie=self.id)
        fields = {}
        for item in mft:
            if item.field.title in fields:
                fields[item.field.title].append(item.tag.title)
            else:
                fields[item.field.title] = [(item.tag.title)]
        
        return fields


class Tag_Field(models.Model):
    tag = models.ForeignKey(Tag)
    field = models.ForeignKey(Field)
    lang = models.CharField(max_length=300)
    title = models.CharField(max_length=300)


    def __str__(self):
        return 'Tag={}, Field={}, Lang={}, Title={}'.format(
            self.tag, self.field, self.lang, self.title)
# class Movie_Field(models.Model):
#     movie = models.ForeignKey(Movie)
#     field = models.ForeignKey(Field)
#     lang = models.CharField(max_length=300)
#     title = models.CharField(max_length=300)


class Movie_Tag_Field(models.Model):
    movie = models.ForeignKey(Movie)
    field = models.ForeignKey(Field)
    tag = models.ForeignKey(Tag)
    
    def __str__(self):
        return 'Movie={}, Field={}, Tag={}'.format(self.movie, self.field, self.tag)


class Collection(models.Model):
    title = models.CharField(max_length=300)
    
    def __str__(self):
        return self.title
    
    def get_items(self):
        return Collection_Movie.objects.filter(collection=self.id)


class Collection_Movie(models.Model):
    collection = models.ForeignKey(Collection)
    movie = models.ForeignKey(Movie)
    
    def __str__(self):
        return 'Collection={}, Movie={}'.format(self.collection, self.movie)


class Languages(object):
    choices = (
        ('he', _('Hebrew')),
        ('en', _('English')),
    )


# class Description(models.Model):
#     movie = models.ForeignKey(Movie, related_name='description')
#     summery = models.TextField()
#     lang = models.CharField(max_length=300, choices=Languages.choices)
#
#     def __str__(self):
#         return 'Movie={}, MovieId={}, Summary={}, Lang={}'.format(self.movie, self.movie.bid, self.summery, self.lang)


class Person(models.Model):
    name_he = models.CharField(max_length=300)
    name_en = models.CharField(max_length=300)
    first_name_he = models.CharField(max_length=300)
    first_name_en = models.CharField(max_length=300)
    last_name_he = models.CharField(max_length=300)
    last_name_en = models.CharField(max_length=300)
