from django.db import models


class Tag(models.Model):
    tid = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    type1_id = models.CharField(max_length=300, blank=True)

    def __str__(self):
        return self.title

class Field(models.Model):
    fid = models.CharField(unique=True, max_length=300)
    title = models.CharField(max_length=300)

    def __str__(self):
        return self.title

class Movie(models.Model):
    bid = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    year = models.IntegerField(null=True, blank=True)
    lang = models.CharField(max_length=300)

    def __str__(self):
        return self.title

    def get_extra_data(self):
        mft = Movie_Tag_Field.objects.filter(movie=self.id)
        fields = {}
        for item in mft:
            if item.field.title in fields:
                fields[item.field.title].append(item.tag.title)
            else:
                fields[item.field.title] = [(item.tag.title)]

        return fields

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


class Description(models.Model):
    movie = models.ForeignKey(Movie)
    summery = models.TextField()
    lang = models.CharField(max_length=300)

    def __str__(self):
        return self.movie