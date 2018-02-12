from django.views import generic

import curation.models
from ifx.base_views import IFXMixin
from curation.forms import CollectionForm


class CollectionMixin(IFXMixin):
    model = curation.models.Collection


class CollectionListView(CollectionMixin, generic.ListView):
    pass


class CollectionDetailView(CollectionMixin, generic.DetailView):
    pass


class CollectionCreateView(CollectionMixin, generic.CreateView):
    form_class = CollectionForm
