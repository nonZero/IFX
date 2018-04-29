from django import forms
from django.utils.translation import ugettext_lazy as _

from ifx.forms import PostToWikiDataForm
from .models import Movie

MOVIE_FIELDS = (
    'year',
    'duration',
    'title_he',
    'title_en',
)

MERGE_FIELDS = MOVIE_FIELDS + (
    'summary_he',
    'summary_en',
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


class PostMovieToWikiDataForm(PostToWikiDataForm):
    year = forms.BooleanField(label=_("year"), required=False, initial=True)
    duration = forms.BooleanField(label=_("duration"), required=False,
                                  initial=True)
