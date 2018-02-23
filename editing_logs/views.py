import django_filters
from django_filters.views import FilterView

from editing_logs.models import LogItem
from ifx.base_views import IFXMixin


class LogItemFilter(django_filters.FilterSet):
    class Meta:
        model = LogItem
        fields = (
            'user',
        )


class LogItemListView(IFXMixin, FilterView):
    template_name = "editing_logs/logitem_list.html"
    filterset_class = LogItemFilter
    model = LogItem
    paginate_by = 25
