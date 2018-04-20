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
