from builtins import super

from django.db.models import Count
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, DetailView

from ifx.base_views import IFXMixin
from movies.models import Movie, Tag, Field
from django.utils.translation import ugettext_lazy as _


class HomePage(IFXMixin, TemplateView):
    template_name = 'movies/homePage.html'
    jumbotron = 'movies/main_jumbotron.html'
    title = _("Home")


class AboutView(IFXMixin, TemplateView):
    template_name = "movies/about.html"
    jumbotron = "movies/about_jumbotron.html"
    title = _("About")


class MovieListView(IFXMixin, ListView):
    jumbotron = 'movies/searchresult_jumbotron.html'
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


class FieldListView(IFXMixin, ListView):
    model = Field

    def get_queryset(self):
        return Field.objects.annotate(
            movie_count=Count('movietagfield')
        ).filter(movie_count__gt=0)


class FieldDetailView(IFXMixin, DetailView):
    breadcrumbs = (
        (_("Fields"), reverse_lazy("movies:field_list")),
    )

    model = Field


TAG_ORDER_FIELDS = {
    'title',
    'lang',
    'type_id',
}

class TagDetailView(IFXMixin, DetailView):
    model = Tag

    def get_breadcrumbs(self):
        fld = self.get_object().movietagfield_set.first().field
        return FieldDetailView.breadcrumbs + (
            (str(fld), fld.get_absolute_url()),
        )

