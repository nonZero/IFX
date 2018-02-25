from django import forms
from django.core.validators import RegexValidator


class WikiDataQValidator(RegexValidator):
    regex = r"^Q[1-9][0-9]+$"


class WikiDataIDForm(forms.Form):
    wikidata_id = forms.CharField(max_length=100,
                                  validators=[WikiDataQValidator])
