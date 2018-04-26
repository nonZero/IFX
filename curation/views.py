from django.views import generic

import curation.models
from curation.forms import CollectionForm
from ifx.base_views import DataContributorOnlyMixin


class CollectionMixin(DataContributorOnlyMixin):
    model = curation.models.Collection


class CollectionListView(CollectionMixin, generic.ListView):
    pass


class CollectionDetailView(CollectionMixin, generic.DetailView):
    pass


class CollectionCreateView(CollectionMixin, generic.CreateView):
    form_class = CollectionForm
