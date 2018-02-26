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


admin.site.register(models.User, UserAdmin)
