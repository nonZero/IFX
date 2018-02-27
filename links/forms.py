from django import forms
from django.utils.translation import ugettext_lazy as _

from general.fields import LocaleModelChoiceField
from links.models import LinkType, Link

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
    'active',
)


class LinkForm(forms.ModelForm):
    type = LocaleModelChoiceField(LinkType.objects.all(), label=_('Type'))

    class Meta:
        model = Link
        fields = FIELDS
