import logging
from builtins import super

import django_filters
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, DetailView, \
    UpdateView, FormView
from django.views.generic.detail import BaseDetailView
from django_filters.views import FilterView

from editing_logs.api import Recorder
from general.templatetags.ifx import bdtitle
from ifx.base_filters import WikidataEntityFilter
from ifx.base_views import IFXMixin, EntityActionMixin, \
    DataContributorOnlyMixin, PostToWikiDataView
from movies import forms
from movies.models import Movie, Tag, Field
from wikidata_edit.upload import upload_movie

logger = logging.getLogger(__name__)


def get_tags():
    return ((t.id, f"{bdtitle(t)} ({t.movie_count})") for t in
            Field.objects.get(idea_fid='AJAN').tags.annotate(
                movie_count=Count('movies')).order_by('title_he'))


class MovieFilter(WikidataEntityFilter):
    title = django_filters.CharFilter(method='title_filter', label=_("title"))
    year = django_filters.RangeFilter()
    duration = django_filters.RangeFilter()
    tags__tag = django_filters.ChoiceFilter(choices=get_tags, label=_("Genre"))
    summary = django_filters.CharFilter(method='summary_filter',
                                        label=_("summary"))

    ordering = django_filters.OrderingFilter(

        label=_("ordering"),
        fields=(
            ('title_he', 'title_he'),
            ('title_en', 'title_en'),
            ('year', 'year'),
            ('duration', 'duration'),
        ),

        field_labels={
            'title_he': _('Hebrew Title (A -> Z)'),
            'title_en': _('English Title (A -> Z)'),
            'year': _('Year (Old -> New)'),
            'duration': _('Duration (Short -> long)'),
            '-title_he': _('Hebrew title (Z -> A)'),
            '-title_en': _('English title (Z -> A)'),
            '-year': _('Year (New -> Old)'),
            '-duration': _('Duration (Long -> Short)'),
        }
    )

    class Meta:
        model = Movie
        fields = (
            'title',
            'year',
            'duration',
            'tags__tag',
        )

    def title_filter(self, queryset, name, value):
        q = Q(title_en__icontains=value) | Q(title_he__icontains=value)
        return queryset.filter(q)

    def summary_filter(self, queryset, name, value):
        q = Q(summary_en__icontains=value) | Q(summary_he__icontains=value)
        return queryset.filter(q)


class MovieListView(IFXMixin, FilterView):
    filterset_class = MovieFilter
    template_name = "movies/movie_list.html"
    model = Movie
    paginate_by = 25
    ordering = "title_he"
    queryset = Movie.objects.active()


class MovieDetailView(IFXMixin, DetailView):
    model = Movie

    breadcrumbs = (
        (_("Movies"), reverse_lazy("movies:list")),
    )

    def predispatch(self):
        if not self.get_object().active and not self.request.user.is_editor():
            raise PermissionDenied()
        super().predispatch()

    def possible_duplicates(self):
        q = Q()
        if self.object.title_he:
            q |= Q(title_he=self.object.title_he)
        if self.object.title_en:
            q |= Q(title_en=self.object.title_en)
        if not q:
            return None
        return Movie.objects.filter(q, active=True).exclude(id=self.object.id)


class MovieUpdateView(DataContributorOnlyMixin, UpdateView):
    model = Movie
    breadcrumbs = MovieDetailView.breadcrumbs
    form_class = forms.MovieForm


class PostMovieToWikiDataView(PostToWikiDataView):
    model = Movie
    breadcrumbs = MovieDetailView.breadcrumbs
    action_name = _("Upload to WikiData")
    fields = forms.MOVIE_FIELDS
    link_type_key = 'for_movies'

    def get_initial(self):
        o = self.get_object()
        d = super().get_initial()
        d['desc_en'] = f"{o.year} Israeli film" if o.year else "Israeli film"
        d['desc_he'] = f"סרט ישראלי משנת {o.year}" if o.year else "סרט ישראלי"
        return d

    def upload(self, d, ids, o):
        labels = {}
        if d['title_he']:
            labels['he'] = o.title_he
        if d['title_en']:
            labels['en'] = o.title_en
        descs = {}
        if d['desc_he']:
            descs['he'] = d['desc_he']
        if d['desc_en']:
            descs['en'] = d['desc_en']
        duration = o.duration if d['duration'] else None
        year = o.year if d['year'] else None
        resp = upload_movie(self.request.user.get_wikidata_oauth1(),
                            labels, descs, ids, year,
                            duration)
        return resp


class MergeIntoView(EntityActionMixin, BaseDetailView, FormView):
    model = Movie
    breadcrumbs = MovieDetailView.breadcrumbs
    action_name = _("Merge into another movie")
    form_class = forms.forms.Form
    template_name = "movies/movie_merge.html"

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.other = get_object_or_404(Movie, pk=self.kwargs['other'])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        o = self.object  # type: Movie
        if o.wikidata_id and not self.other.wikidata_id:
            form.fields['wikidata_id'] = forms.forms.BooleanField(
                required=False, initial=True,
                label=_("WikiData ID"))

        for fld in forms.MERGE_FIELDS:
            v = getattr(o, fld)
            old = getattr(self.other, fld)
            if v and v != old:
                form.fields[fld] = forms.forms.BooleanField(
                    required=False, help_text=v, initial=not old,
                    label=o._meta.get_field(fld).verbose_name)

        for t in o.tags.all():
            k = f"t_{t.id}"
            form.fields[k] = forms.forms.BooleanField(
                required=False, initial=True,
                label=f"{bdtitle(t.tag.field)} > {bdtitle(t.tag)}")

        for r in o.people.all():
            k = f"r_{r.id}"
            form.fields[k] = forms.forms.BooleanField(
                required=False, initial=True,
                label=f"{bdtitle(r.role)} > {bdtitle(r.person)}")

        return form

    def form_valid(self, form):
        o = self.object  # type: Movie
        d = form.cleaned_data

        with Recorder(user=self.request.user, note="merge") as r:
            r.record_update_before(o)

            if o.wikidata_id and not self.other.wikidata_id and d[
                'wikidata_id']:
                self.other.wikidata_id = o.wikidata_id
                o.wikidata_id = None
                self.other.wikidata_status = o.wikidata_status
                o.wikidata_status = o.Status.NOT_APPLICABLE

            o.active = False
            o.merged_into = self.other
            o.save()
            r.record_update_after(o)
            o.suggestions.all().delete()

            for fld in forms.MERGE_FIELDS:
                v = getattr(o, fld)
                old = getattr(self.other, fld)
                if v and v != old and d[fld]:
                    setattr(self.other, fld, v)
                    self.other.idea_modified = True

            r.record_update_before(o.__class__.objects.get(pk=self.other.pk))
            self.other.save()
            r.record_update_after(self.other)

            for t in o.tags.all():
                k = f"t_{t.id}"
                if d[k]:
                    tag, created = self.other.tags.get_or_create(tag=t.tag)
                    if created:
                        r.record_addition(tag)

            for ro in o.people.all():
                k = f"r_{ro.id}"
                if d[k]:
                    mrp, created = self.other.people.get_or_create(
                        role=ro.role, person=ro.person,
                        defaults={'priority': ro.priority, 'note': ro.note}
                    )
                    if created:
                        r.record_addition(mrp)
                if ro.active:
                    r.record_update_before(ro)
                    ro.active = False
                    ro.save()
                    r.record_update_after(ro)

            for l in o.links.all():
                r.record_update_before(l)
                l.entity = self.other
                l.save()
                r.record_update_after(l)

        messages.success(self.request, _("Merged."))

        return redirect(o)


class FieldListView(IFXMixin, ListView):
    model = Field

    def get_queryset(self):
        return Field.objects.annotate(
            movie_count=Count('tags__movies')).filter(
            movie_count__gt=0)


class FieldDetailView(IFXMixin, DetailView):
    breadcrumbs = (
        (_("Fields"), reverse_lazy("movies:field_list")),
    )

    model = Field


TAG_ORDER_FIELDS = {
    'title_he',
    'title_en',
    'lang',
    'type_id',
}


class TagDetailView(IFXMixin, DetailView):
    model = Tag

    def get_breadcrumbs(self):
        fld = self.get_object().field
        return FieldDetailView.breadcrumbs + (
            (str(fld), fld.get_absolute_url()),
        )
