from django.views.generic import ListView, DetailView

from ifx.base_views import IFXMixin
from people.models import Person


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


PERSON_ORDER_FIELDS = {
    'name_he',
    'name_en',
    'first_name_he',
    'first_name_en',
    'last_name_he',
    'last_name_en',
}
