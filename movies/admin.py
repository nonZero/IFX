from django.contrib import admin
from . import models

admin.site.register(models.Movie)
admin.site.register(models.Tag)
admin.site.register(models.Field)
admin.site.register(models.Movie_Tag_Field)
admin.site.register(models.Collection)
admin.site.register(models.Collection_Movie)
