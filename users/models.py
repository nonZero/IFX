from authtools.models import AbstractEmailUser
from django.db import models
from django.utils.translation import ugettext_lazy as _


class User(AbstractEmailUser):
    name_he = models.CharField(_('Hebrew full name (for display)'),
                               max_length=500,
                               blank=True, null=True)
    name_en = models.CharField(_('English full name (for display)'),
                               max_length=500,
                               blank=True, null=True)
    full_name_he = models.CharField(_('Hebrew full name'), max_length=500,
                                    blank=True, null=True)
    full_name_en = models.CharField(_('English full name'), max_length=500,
                                    blank=True, null=True)
    bio_he = models.TextField(_('Personal bio in Hebrew(, public)'),
                              blank=True,
                              null=True)

    bio_en = models.TextField(_('Personal bio in English(, public)'),
                              blank=True,
                              null=True)

    is_team_member = models.BooleanField(_('team member'), default=False)
    is_data_volunteer = models.BooleanField(_('data volunteer'), default=False)
