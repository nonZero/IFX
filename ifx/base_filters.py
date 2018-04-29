import django_filters
from django.utils.translation import ugettext_lazy as _
from django_filters import FilterSet


class WikidataEntityFilter(FilterSet):
    has_wikidata_id = django_filters.BooleanFilter(
        method='has_wikidata_id_filter', label=_("has wikidata id"))

    def has_wikidata_id_filter(self, queryset, name, value):
        return queryset.filter(wikidata_id__isnull=not value)