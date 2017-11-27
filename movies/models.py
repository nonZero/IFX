from django.db import models


class Movie(models.Model):
    date = models.DateField()
    length = models.DecimalField(max_digits=12, decimal_places=2)
    title = models.CharField(max_length=300)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title
