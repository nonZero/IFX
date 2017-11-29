from django import forms

from movies.models import Movie


class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = "__all__"


class MyForm(forms.Form):
    title = forms.CharField(max_length=123)
    agree_tos = forms.BooleanField()

