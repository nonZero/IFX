from django import forms
from django.utils.translation import ugettext_lazy as _


class PostToWikiDataForm(forms.Form):
    name_he = forms.BooleanField(label=_("Hebrew name"), required=False,
                                  initial=True)
    name_en = forms.BooleanField(label=_("English name"), required=False,
                                  initial=True)
    desc_he = forms.CharField(label=_("Hebrew description"), required=False)
    desc_en = forms.CharField(label=_("English description"), required=False)