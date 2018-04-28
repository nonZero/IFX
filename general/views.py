from pathlib import Path

import markdown
from django.conf import settings
from django.utils import translation
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView

from ifx.base_views import IFXMixin
from movies.models import Movie
from people.models import Person


class HomePage(IFXMixin, TemplateView):
    template_name = 'home.html'
    jumbotron = 'movies/main_jumbotron.html'
    title = _("Home")

    def random_movies(self, n=3):
        return Movie.objects.active().order_by("?")[:n]

    def random_people(self, n=8):
        return Person.objects.active().exclude(movies=None).order_by("?")[:n]


class AboutView(IFXMixin, TemplateView):
    template_name = "movies/about.html"
    jumbotron = "movies/about_jumbotron.html"
    title = _("About")

    def get_html_content(self):
        lang = translation.get_language()[:2]
        with (Path(settings.BASE_DIR) / f"about_{lang}.md").open() as f:
            return mark_safe(markdown.markdown(f.read()))
