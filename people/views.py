import django_filters
from django.db.models import Q
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, UpdateView
from django_filters.views import FilterView

from ifx.base_views import IFXMixin, EntityEditMixin
from people.models import Person
from . import forms


class PersonFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(method='name_filter', label=_("name"))

    class Meta:
        model = Person
        fields = ()

    def name_filter(self, queryset, name, value):
        q = Q(name_en__icontains=value) | Q(name_he__icontains=value)
        return queryset.filter(q)


class PersonListView(IFXMixin, FilterView):
    template_name = "people/person_list.html"
    filterset_class = PersonFilter
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
