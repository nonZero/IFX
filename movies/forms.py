from django import forms

from movies.models import Movie, Collection


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = "__all__"


class SearchByYearForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['year',]
