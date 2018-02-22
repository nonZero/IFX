from django.shortcuts import get_object_or_404
from django.views.generic import CreateView

from ifx.base_views import IFXMixin
from links.models import MovieLink
from movies.models import Movie


class MovieLinkCreateView(IFXMixin, CreateView):
    model = MovieLink
    fields = (
        'type',
        'value',
        'title_he',
        'title_en',
        'notes_he',
        'notes_en',
        'language',
        'limit_to_language',
        'editing_comment',
    )

    def dispatch(self, request, *args, **kwargs):
        self.movie = get_object_or_404(Movie, pk=kwargs['movie_pk'])
        return super().dispatch(request, *args, **kwargs)


