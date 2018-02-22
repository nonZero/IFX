from django.contrib import admin

from . import models


class RoleAdmin(admin.ModelAdmin):
    list_display = (
        'idea_tid',
        'title_en',
        'title_he',
        'appears_in_short_version',
        'short_version_order',
    )


admin.site.register(models.Person)
admin.site.register(models.Role, RoleAdmin)
