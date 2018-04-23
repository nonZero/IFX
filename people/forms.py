from django import forms
from django.utils.translation import ugettext_lazy as _

from .models import Person

PERSON_FIELDS = (
    'name_he',
    'name_en',
)

MERGE_FIELDS = PERSON_FIELDS + (
    'first_name_he',
    'first_name_en',
    'last_name_he',
    'last_name_en',
)


class PersonForm(forms.ModelForm):
    editing_comment = forms.CharField(label=_('Editing Comment'),
                                      widget=forms.Textarea)

    class Meta:
        model = Person
        fields = PERSON_FIELDS
