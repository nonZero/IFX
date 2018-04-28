import authtools.admin
from authtools.forms import AdminUserChangeForm
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
        'password',
    )
})


class FixedChangeForm(AdminUserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].help_text = self.fields[
            'password'].help_text.format('../password/')


class UserAdmin(authtools.admin.UserAdmin):
    form = FixedChangeForm
    fieldsets = (
        BASE_FIELDS,
        authtools.admin.ADVANCED_PERMISSION_FIELDS,
        authtools.admin.DATE_FIELDS,
    )
    list_display = (
        'email',
        'name_he',
        'name_en',
        'full_name_he',
        'full_name_en',
        'is_active',
        'is_data_volunteer',
        'is_team_member',
        'is_staff',
        'is_superuser',
        'date_joined',
        'last_login',
        'wikidata_access_token_created_at',
    )
    list_filter = (
        'is_superuser',
        'is_staff',
        'is_team_member',
        'is_data_volunteer',
        'is_active',
    )
    search_fields = (
        'id',
        'email',
        'name_he',
        'name_en',
        'full_name_he',
        'full_name_en',

    )


admin.site.register(models.User, UserAdmin)
