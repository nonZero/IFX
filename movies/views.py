from builtins import super

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView, DetailView, UpdateView

from editing_logs.api import Recorder
from enrich.lookup import create_suggestion
from enrich.tasks import lookup_suggestion_by_id
from ifx.base_views import IFXMixin
from movies import forms
from movies.models import Movie, Tag, Field
from people.models import Person


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
