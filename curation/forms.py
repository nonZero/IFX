from django import forms

from curation.models import Collection


class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = "__all__"