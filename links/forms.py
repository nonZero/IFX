from django import forms
from django.utils.translation import ugettext_lazy as _

from general.fields import LocaleModelChoiceField
from links.models import MovieLink, PersonLink, LinkType

FIELDS = (
    'type',
    'value',
    'title_he',
    'title_en',
    'notes_he',
    'notes_en',
    'language',
    'limit_to_language',
    'editing_comment',
)


class MovieLinkForm(forms.ModelForm):
    type = LocaleModelChoiceField(LinkType.objects.filter(for_movies=True),
                                  label=_('Type'))

    class Meta:
        model = MovieLink
        fields = FIELDS


class PersonLinkForm(forms.ModelForm):
    type = LocaleModelChoiceField(LinkType.objects.filter(for_people=True),
                                  label=_('Type'))

    class Meta:
        model = PersonLink
        fields = FIELDS
