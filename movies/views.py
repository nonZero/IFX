import json
import logging
from builtins import super

import django_filters
from django.contrib import messages
from django.db.models import Count, Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView, DetailView, \
    UpdateView, FormView
from django.views.generic.detail import BaseDetailView
from django_filters.views import FilterView

from general.templatetags.ifx import bdtitle
from ifx.base_views import IFXMixin, EntityEditMixin, EntityActionMixin
from links.models import LinkType
from links.tasks import add_links_by_movie_id
from movies import forms
from movies.models import Movie, Tag, Field
from people.models import Person
from wikidata_edit.upload import upload_movie

logger = logging.getLogger(__name__)


class HomePage(IFXMixin, TemplateView):
    template_name = 'home.html'
    jumbotron = 'movies/main_jumbotron.html'
    title = _("Home")

    def random_movies(self, n=3):
        return Movie.objects.order_by("?")[:n]

    def random_people(self, n=8):
        return Person.objects.exclude(movies=None).order_by("?")[:n]


class AboutView(IFXMixin, TemplateView):
    template_name = "movies/about.html"
    jumbotron = "movies/about_jumbotron.html"
    title = _("About")


def get_tags():
    return ((t.id, f"{bdtitle(t)} ({t.movie_count})") for t in
            Field.objects.get(idea_fid='AJAN').tags.annotate(
                movie_count=Count('movies')).order_by('title_he'))


class MovieFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(method='title_filter', label=_("title"))
    year = django_filters.RangeFilter()
    duration = django_filters.RangeFilter()
    tags__tag = django_filters.ChoiceFilter(choices=get_tags, label=_("Genre"))

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


class MovieListView(IFXMixin, FilterView):
    filterset_class = MovieFilter
    template_name = "movies/movie_list.html"
    model = Movie
    paginate_by = 25
    ordering = "title_he"


class MovieDetailView(IFXMixin, DetailView):
    model = Movie

    breadcrumbs = (
        (_("Movies"), reverse_lazy("movies:list")),
    )


class MovieUpdateView(EntityEditMixin, UpdateView):
    model = Movie
    breadcrumbs = MovieDetailView.breadcrumbs
    form_class = forms.MovieForm


class PostToWikiDataView(EntityActionMixin, BaseDetailView, FormView):
    model = Movie
    breadcrumbs = MovieDetailView.breadcrumbs
    action_name = _("Upload to WikiData")
    form_class = forms.PostToWikiDataForm
    template_name = "movies/movie_upload.html"

    def get_initial(self):
        o = self.get_object()
        d = super().get_initial()
        d['desc_en'] = f"{o.year} Israeli film" if o.year else "Israeli film"
        d['desc_he'] = f"סרט ישראלי משנת {o.year}" if o.year else "סרט ישראלי"
        return d

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        for fld in forms.MOVIE_FIELDS:
            form.fields[fld].help_text = getattr(self.object, fld)
        for lt in LinkType.objects.filter(for_movies=True,
                                          wikidata_id__isnull=False):
            k = f'ext_{lt.wikidata_id}'
            form.fields[k] = forms.forms.CharField(label=bdtitle(lt),
                                                   required=False, help_text=_(
                    "ID only! (do not enter full URL)"))
        return form

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        o = self.object  # type: Movie
        d = form.cleaned_data

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

        ids = {}
        qs = LinkType.objects.filter(for_movies=True,
                                     wikidata_id__isnull=False)
        for lt in qs:
            k = f'ext_{lt.wikidata_id}'
            if d[k]:
                ids[lt.wikidata_id] = d[k]

        resp = upload_movie(self.request.user.get_wikidata_oauth1(),
                            labels, descs, ids, year,
                            duration)
        if resp.get('success') != 1:
            msg = "Error uploading data to wikidata\n"
            logger.error(msg + json.dumps(resp, indent=2))
            messages.error(self.request, msg)
        else:
            o.wikidata_id = resp['entity']['id']
            o.wikidata_status = o.Status.ASSIGNED
            o.save()
            messages.success(self.request, _("Added new wikidata entity."))
            add_links_by_movie_id(o.id)
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
