import json
import logging
from builtins import super

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView, DetailView, \
    UpdateView, FormView
from django.views.generic.detail import BaseDetailView

from editing_logs.api import Recorder
from enrich.lookup import create_suggestion
from enrich.tasks import lookup_suggestion_by_id
from general.templatetags.ifx import bdtitle
from ifx.base_views import IFXMixin
from links.models import LinkType
from links.tasks import add_links_by_movie_id
from movies import forms
from movies.models import Movie, Tag, Field
from wikidata_edit.upload import upload_movie
from people.models import Person

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


class MovieListView(IFXMixin, ListView):
    # jumbotron = 'movies/searchresult_jumbotron.html'
    model = Movie
    paginate_by = 25

    ORDER_FIELDS = {
        'title_he',
        'title_en',
        'year',
    }

    DEFAULT_ORDER_FIELD = "title_he"

    def get_ordering(self):
        k = self.request.GET.get('order', None)
        if k not in self.ORDER_FIELDS:
            k = self.DEFAULT_ORDER_FIELD
        return k


class MovieDetailView(IFXMixin, DetailView):
    model = Movie

    breadcrumbs = (
        (_("Movies"), reverse_lazy("movies:list")),
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['set_jumbotron'] = 3
        return context


class MovieUpdateView(IFXMixin, UpdateView):
    model = Movie
    form_class = forms.MovieForm

    breadcrumbs = (
        (_("Movies"), reverse_lazy("movies:list")),
    )

    def form_valid(self, form):
        o = form.instance
        original = o.__class__.objects.get(id=o.id)
        if any(getattr(o, attr) != getattr(original, attr) for attr in
               forms.MOVIE_FIELDS):
            with Recorder(user=self.request.user,
                          note=form.cleaned_data['editing_comment']) as r:
                r.record_update_before(original)
                form.save()
                r.record_update_after(o)
            messages.success(self.request, _("Movie updated successfully"))
            if o.title_he:
                s, created = create_suggestion(o)
                lookup_suggestion_by_id.delay(s.id)
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


class PostToWikiDataView(IFXMixin, BaseDetailView, FormView):
    model = Movie
    form_class = forms.PostToWikiDataForm
    template_name = "movies/movie_upload.html"

    def get(self, request, *args, **kwargs):
        if self.request.user.wikidata_access_token is None:
            redirect(f'{reverse("users:oauth")}?return_to={self.request.path}')
        return super().get(request, *args, **kwargs)

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
        if resp['success'] != 1:
            msg = f"Invalid success code: {resp['success']} != 1:"
            logger.error(msg + "\n" + json.dumps(resp, indent=2))
            messages.error(self.request, msg)
        else:
            o.wikidata_id = resp['entity']['id']
            o.wikidata_status = o.Status.ASSIGNED
            o.save()
            messages.success(self.request, _("Added new wikidata entity."))
            add_links_by_movie_id(o.id)
        return redirect(o)
