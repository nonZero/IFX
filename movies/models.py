from django.db import models


class Tag(models.Model):
    tid = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    type1_id = models.CharField(max_length=300)

    def __str__(self):
        return self.title


class Movie(models.Model):
    bid = models.IntegerField(unique=True)
    title = models.CharField(max_length=300)
    year = models.IntegerField(null=True, blank=True)
    length = models.DecimalField(null=True, blank=True, max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)

    tags = models.ManyToManyField(Tag, blank=True, related_name="movies")

    def __str__(self):
        return self.title