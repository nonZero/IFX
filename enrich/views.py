import django_filters
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django_filters.views import FilterView

from editing_logs.api import Recorder
from enrich.models import Suggestion
from enrich.tasks import lookup_suggestion_by_id
from ifx.base_models import WikiDataEntity
from ifx.base_views import IFXMixin
from . import forms


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


class SetWikiDataIDView(IFXMixin, SingleObjectMixin, View):
    model = Suggestion

    def post(self, request, *args, **kwargs):
        # TODO: check permissions
        s = self.get_object()  # type: Suggestion
        o = s.entity
        form = forms.WikiDataIDForm(request.POST)
        if form.is_valid():
            if o.wikidata_id != form.cleaned_data['wikidata_id']:
                try:
                    with Recorder(user=self.request.user) as r:
                        r.record_update_before(o)
                        o.wikidata_status = WikiDataEntity.Status.ASSIGNED
                        o.wikidata_id = form.cleaned_data['wikidata_id']
                        o.save()
                        r.record_update_after(o)

                        s.status = s.Status.VERIFIED
                        s.save()

                    # TODO: fetch wikidata info
                    messages.success(request, _("Wikidata ID assigned."))
                except IntegrityError:
                    messages.error(request, _("Wikidata ID already exists!"))
        else:
            messages.error(request, _("Invalid form"))

        return redirect(o)
