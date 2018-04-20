import django_filters
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django_filters.views import FilterView

from editing_logs.models import LogItem
from ifx.base_views import IFXMixin
from movies.models import Movie


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
    queryset = LogItem.objects.order_by('-created_at')


class MovieLogItemListView(LogItemListView):
    def get_queryset(self):
        self.movie = get_object_or_404(Movie, pk=self.kwargs['pk'])
        ct = ContentType.objects.get_for_model(Movie)
        qs = super().get_queryset().filter(rows__content_type=ct,
                                           rows__object_id=self.movie.id)
        return qs
