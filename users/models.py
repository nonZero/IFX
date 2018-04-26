from authtools.models import AbstractEmailUser
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from mwoauth import AccessToken
from requests_oauthlib import OAuth1


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

    wikidata_access_token_created_at = models.DateTimeField(null=True)
    wikidata_access_token = JSONField(null=True)

    def __str__(self):
        lang = translation.get_language()[:2]
        lang2 = {'en': 'he', 'he': 'en'}[lang]
        return (getattr(self, f"name_{lang}")
                or getattr(self, f"name_{lang2}") or f"#{self.id}")

    def get_access_token(self):
        if self.wikidata_access_token is None:
            return None
        return AccessToken(self.wikidata_access_token['key'].encode(),
                           self.wikidata_access_token['secret'].encode())

    def get_wikidata_oauth1(self):
        auth1 = OAuth1(settings.OAUTH_CONSUMER_KEY,
                       settings.OAUTH_CONSUMER_SECRET,
                       resource_owner_key=self.wikidata_access_token['key'],
                       resource_owner_secret=self.wikidata_access_token[
                           'secret'])
        return auth1

    def is_editor(self):
        return self.is_superuser or self.is_data_volunteer
