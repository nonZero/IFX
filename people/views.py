from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, UpdateView

from ifx.base_views import IFXMixin, EntityEditMixin
from people.models import Person
from . import forms


class PersonListView(IFXMixin, ListView):
    model = Person
    paginate_by = 50

    def get_queryset(self):
        return super().get_queryset().filter(movies__isnull=False).distinct()

    def get_ordering(self):
        k = self.request.GET.get('order', None)
        if k not in PERSON_ORDER_FIELDS:
            k = "name_he"
        return k


class PersonDetailView(IFXMixin, DetailView):
    model = Person

    breadcrumbs = (
        (_("People"), reverse_lazy("people:list")),
    )


PERSON_ORDER_FIELDS = {
    'name_he',
    'name_en',
    'first_name_he',
    'first_name_en',
    'last_name_he',
    'last_name_en',
}


class PersonUpdateView(EntityEditMixin, UpdateView):
    model = Person
    breadcrumbs = PersonDetailView.breadcrumbs
    form_class = forms.PersonForm
    template_name = "generic_form.html"
