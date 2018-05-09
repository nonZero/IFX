import difflib
import logging
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from typing import Iterable

from general.templatetags.ifx import ut_plus
from ifx.base_views import DataContributorOnlyMixin
from movies.models import Movie
from reports.views import BaseReport
from . import models

logger = logging.getLogger(__name__)


def get_titles():
    q = Q(title_he__isnull=False) | Q(title_en__isnull=False)
    for m in Movie.objects.filter(q):  # type: Movie
        if m.title_he:
            assert m.title_he
            yield m.title_he
        if m.title_en:
            assert m.title_en
            yield m.title_en


def get_my_close_matches(words, possibilities, cutoff=0.75):
    if not 0.0 <= cutoff <= 1.0:
        raise ValueError("cutoff must be in [0.0, 1.0]: %r" % (cutoff,))

    s = difflib.SequenceMatcher()
    for word in words:
        s.set_seq2(word)
        for x in possibilities:
            s.set_seq1(x)
            if s.real_quick_ratio() >= cutoff and s.quick_ratio() >= cutoff:
                n = s.ratio()
                if n >= cutoff:
                    yield n, x


def find_candidates(titles, v):
    words = filter(None, (v.title_he, v.title_en))
    near = sorted(get_my_close_matches(words, titles), reverse=True)[:8]
    return [(n, t, Movie.objects.filter(Q(title_he=t) | Q(title_en=t))) for
            n, t in near]


def add_candidates(qs: Iterable[models.VendorItem]):
    titles = sorted(set(get_titles()))

    for v in qs:
        if not v.entity:
            v.candidates = find_candidates(titles, v)
        yield v


class VendorDataListView(BaseReport):
    template_name = "vendor_data/vendordata_list.html"

    cols = (
        '#',
        # _("Vendor"),
        _("Vendor ID"),
        # _("Type"),
        _("Status"),
        _("Hebrew Title"),
        _("English Title"),
        _("Year"),
        _("Duration"),
        _("Entity / Candidates"),
    )
    model = models.VendorItem

    def get_queryset(self):
        qs = super().get_queryset()
        return list(add_candidates(qs))


class SetVendorItemEntityView(DataContributorOnlyMixin, SingleObjectMixin,
                              View):
    model = models.VendorItem

    def post(self, request, *args, **kwargs):
        o = self.get_object()  # type: models.VendorItem
        en = get_object_or_404(Movie, pk=kwargs['entity_id'])

        if o.entity is None:
            o.entity = en
            o.status = o.Status.ASSIGNED
            o.save()
        return JsonResponse({'html': ut_plus(o.entity)})
