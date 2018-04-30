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
    title_he = forms.BooleanField(label=_("Hebrew title"), required=False,
                                  initial=True)
    title_en = forms.BooleanField(label=_("English title"), required=False,
                                  initial=True)
    year = forms.BooleanField(label=_("year"), required=False, initial=True)
    duration = forms.BooleanField(label=_("duration"), required=False,
                                  initial=True)
