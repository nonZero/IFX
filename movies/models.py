from django.db import models


class Movie(models.Model):
    bid = models.IntegerField()
    date = models.DateField()
    length = models.DecimalField(max_digits=12, decimal_places=2)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

class Tag(models.Model):
    tid = models.IntegerField()
    title = models.CharField(max_length=300)
    type1_id = models.CharField(max_length=300)

    def __str__(self):
        return self.title
