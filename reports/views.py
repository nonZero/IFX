from django.db.models import Count
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic import ListView, TemplateView

from ifx.base_views import DataContributorOnlyMixin
from movies.models import Movie
from people.models import Person

REPORTS = []


def add_report(key):
    def df(view):
        REPORTS.append((key, view))
        return view

    return df


class BaseReport(DataContributorOnlyMixin, ListView):
    breadcrumbs = (
        (_("Reports"), reverse_lazy("reports:list")),
    )


class MovieReport(BaseReport):
    template_name = "reports/movie_report.html"
    cols = (
        '#',
        _("Hebrew Title"),
        _("English Title"),
        _("Year"),
        mark_safe('<span class="fa fa-barcode"></span>'),
        _("Legacy ID"),
    )


@add_report('all-movies')
class NoTitleMovieReport(MovieReport):
    title = _("All Movies")
    model = Movie


@add_report('no-title')
class NoTitleMovieReport(MovieReport):
    title = _("Missing Titles")

    def get_queryset(self):
        return Movie.objects.filter(title_he=None)


@add_report('no-english-title')
class NoEnglishTitleMovieReport(MovieReport):
    title = _("Missing English Titles")

    def get_queryset(self):
        return Movie.objects.filter(title_en=None)


@add_report('no-year')
class NoYearMovieReport(MovieReport):
    title = _("Missing Years")

    def get_queryset(self):
        return Movie.objects.filter(year=None)


@add_report('dupe-title')
class DuplicateTitleMovieReport(MovieReport):
    title = _("Duplicate Titles")
    duplicate_field = 'title_he'

    def get_queryset(self):
        qs0 = Movie.objects.active().exclude(title_he=None).values(
            self.duplicate_field).annotate(
            x=Count('id')).filter(
            x__gt=1).order_by(self.duplicate_field)
        titles = qs0.values_list(self.duplicate_field, flat=True)
        qs = Movie.objects.filter(title_he__in=titles).order_by(
            self.duplicate_field,
            'year')
        return qs


@add_report('dupe-english-title')
class DuplicateMovieEnglishTitleReport(DuplicateTitleMovieReport):
    title = _("Duplicate English Titles")
    duplicate_field = 'title_en'


class PersonReport(BaseReport):
    template_name = "reports/person_report.html"
    cols = (
        '#',
        _("Hebrew Name"),
        _("English Name"),
        _("Movies"),
        _("Roles"),
        mark_safe('<span class="fa fa-barcode"></span>'),
        _("Legacy ID"),
    )


@add_report('person-missing-name')
class NoNamePersonReport(PersonReport):
    title = _("People without a name")

    def get_queryset(self):
        return Person.objects.filter(name_he=None).annotate(
            role_count=Count('movies')
        ).filter(
            role_count__gte=1
        ).prefetch_related('movies')


class ReportList(DataContributorOnlyMixin, TemplateView):
    title = _("Reports")
    template_name = "reports/reports.html"
    reports = [(f"reports:{k}", v) for k, v in REPORTS]
