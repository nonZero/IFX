from django.views.generic import CreateView

from ifx.base_views import IFXMixin
from links.models import MovieLink


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
