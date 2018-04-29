from django import forms
from django.utils.translation import ugettext_lazy as _

from ifx.forms import PostToWikiDataForm
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


GENDER_CHOICES = (
    (None, '---------'),
    (6581097, _("Female")),
    (6581072, _("Male")),
    (1097630, _("Intersex")),
    (1052281, _("Transgender Female")),
    (2449503, _("Transgender Male")),
)


class PostPersonToWikiDataForm(PostToWikiDataForm):
    gender = forms.TypedChoiceField(choices=GENDER_CHOICES,
                                    coerce=int,
                                    empty_value=None,
                                    label=_("gender"), required=False)
