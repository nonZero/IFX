from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import CreateView

from editing_logs.api import Recorder
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

    # def get_success_url(self):
    #     return redirect(self.movie)
    #
    def dispatch(self, request, *args, **kwargs):
        self.movie = get_object_or_404(Movie, pk=kwargs['movie_pk'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with Recorder(user=self.request.user,
                      note=form.cleaned_data['editing_comment']) as r:
            assert isinstance(form.instance, MovieLink)
            form.instance.parent = self.movie
            form.save()
            r.record_addition(form.instance)
        messages.success(self.request, _("Link added successfully"))
        return redirect(self.movie)
