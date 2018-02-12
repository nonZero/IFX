from django.contrib import admin

import curation.models
from . import models


class FieldAdmin(admin.ModelAdmin):
    list_display = (
        'fid',
        'title',
        'appears_in_short_version',
        'short_version_order',
    )


admin.site.register(models.Movie)
admin.site.register(models.Tag)
admin.site.register(models.Field, FieldAdmin)
admin.site.register(models.MovieTagField)
admin.site.register(curation.models.Collection)
admin.site.register(curation.models.CollectionMovie)
