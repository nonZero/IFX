import django_filters
from django_filters.views import FilterView

from enrich.models import Suggestion
from ifx.base_views import IFXMixin


class SuggestionFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Suggestion
        fields = (
            'status',
            'source',
            'content_type',
            'query',
        )


class SuggestionListView(IFXMixin, FilterView):
    template_name = "enrich/suggestion_list.html"
    filterset_class = SuggestionFilter
    model = Suggestion
    paginate_by = 100
