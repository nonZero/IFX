import re

from django.db.models import Q

from movies.views import MovieListView

YEAR_RANGE_RE = re.compile(r"^(?P<start>(19|20)[0-9][0-9])-(?P<end>(19|20)[0-9][0-9])$")


class MoviesSearchListView(MovieListView):
    def get_queryset(self):
        qs = super(MoviesSearchListView, self).get_queryset()
        query = self.request.GET.get('q')
        search_type = self.request.GET.get('idselect')
        q = self.get_filters(query, search_type)
        qs = qs.filter(q)
        return qs

    def get_filters(self, query, search_type):
        q = (
                Q(title_he__icontains=query) |
                Q(title_en__icontains=query) |
                Q(summary_he__icontains=query) |
                Q(summary_en__icontains=query)
        )
        if query.isdigit():
            q |= Q(year=int(query))
        m = YEAR_RANGE_RE.match(query)
        if m:
            q |= Q(year__gte=m['start'], year__lte=m['start'])

        return q
