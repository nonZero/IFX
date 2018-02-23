import authtools.admin
from django.contrib import admin

from . import models

BASE_FIELDS = (None, {
    'fields': (
        'email',
        'name_he',
        'name_en',
        'full_name_he',
        'full_name_en',
        'bio_he',
        'bio_en',
        'is_team_member',
        'is_data_volunteer',
        'password'
    )
})


class UserAdmin(authtools.admin.UserAdmin):
    fieldsets = (
        BASE_FIELDS,
        authtools.admin.ADVANCED_PERMISSION_FIELDS,
        authtools.admin.DATE_FIELDS,
    )


admin.site.register(models.User, UserAdmin)
