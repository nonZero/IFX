from django.contrib import admin

import curation.models
from . import models


class FieldAdmin(admin.ModelAdmin):
    list_display = (
        'fid',
        'title_he',
        'title_en',
        'appears_in_short_version',
        'short_version_order',
    )


class TagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'field',
        'tid',
        'title_he',
        'title_en',
    )


admin.site.register(models.Movie)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.Field, FieldAdmin)
admin.site.register(models.MovieTag)
admin.site.register(curation.models.Collection)
admin.site.register(curation.models.CollectionMovie)
