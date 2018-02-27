from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import register_converter

from ifx.converters import IFXEntityConverter

register_converter(IFXEntityConverter, 'ifx_entity')

urlpatterns = i18n_patterns(
    url(r'', include("movies.urls")),
    url(r'^people/', include("people.urls")),
    url(r'^search/', include("search.urls")),
    url(r'^collections/', include("curation.urls")),
    url(r'^links/', include("links.urls")),

    url(r'^enrich/', include("enrich.urls")),

    url(r'^logs/', include("editing_logs.urls")),
    url(r'^reports/', include("reports.urls")),

    url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', admin.site.urls),
)
