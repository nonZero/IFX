import django_filters
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django_filters.views import FilterView

from enrich.models import Suggestion
from enrich.tasks import lookup_suggestion_by_id
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


class SuggestionForceLookupView(IFXMixin, SingleObjectMixin, View):
    model = Suggestion

    def post(self, request, *args, **kwargs):
        o = self.get_object()
        o.status = Suggestion.Status.PENDING
        o.result = None
        o.source_key = None
        o.source_url = None
        o.error_message = None
        o.save()
        lookup_suggestion_by_id.delay(o.id)
        messages.info(request, _("Suggestion queued for lookup"))
        return redirect(o.entity)
