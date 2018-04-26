import django_filters
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from django_filters.views import FilterView

from editing_logs.models import LogItem
from general.templatetags.ifx import bdtitle
from ifx.base_views import IFXMixin, DataContributorOnlyMixin


class LogItemFilter(django_filters.FilterSet):
    class Meta:
        model = LogItem
        fields = (
            'user',
        )


class LogItemListView(DataContributorOnlyMixin, FilterView):
    template_name = "editing_logs/logitem_list.html"
    filterset_class = LogItemFilter
    model = LogItem
    paginate_by = 25
    queryset = LogItem.objects.order_by('-created_at')


class EntityLogItemListView(LogItemListView):

    def get_breadcrumbs(self):
        return (
            (bdtitle(self.object), self.object.get_absolute_url()),
        )

    def get_queryset(self):
        model = self.kwargs['model']
        self.object = get_object_or_404(model, pk=self.kwargs['pk'])
        ct = ContentType.objects.get_for_model(model)
        qs = super().get_queryset().filter(rows__content_type=ct,
                                           rows__object_id=self.object.id)
        return qs
