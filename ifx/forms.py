from django import forms
from django.utils.translation import ugettext_lazy as _


class PostToWikiDataForm(forms.Form):
    desc_he = forms.CharField(label=_("Hebrew description"), required=False)
    desc_en = forms.CharField(label=_("English description"), required=False)