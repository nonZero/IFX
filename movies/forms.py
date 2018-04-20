from django import forms
from django.utils.translation import ugettext_lazy as _

from movies.models import Movie

MOVIE_FIELDS = (
    'year',
    'duration',
    'title_he',
    'title_en',
)


class MovieForm(forms.ModelForm):
    editing_comment = forms.CharField(label=_('Editing Comment'),
                                      widget=forms.Textarea)

    class Meta:
        model = Movie
        fields = MOVIE_FIELDS


class SearchByYearForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = [
            'year',
        ]


class PostToWikiDataForm(forms.Form):
    year = forms.BooleanField(label=_("year"), required=False, initial=True)
    duration = forms.BooleanField(label=_("duration"), required=False,
                                  initial=True)
    title_he = forms.BooleanField(label=_("Hebrew title"), required=False,
                                  initial=True)
    title_en = forms.BooleanField(label=_("English title"), required=False,
                                  initial=True)
    desc_he = forms.CharField(label=_("Hebrew description"), required=False,
                                  initial=True)
    desc_en = forms.CharField(label=_("English description"), required=False,
                                  initial=True)
