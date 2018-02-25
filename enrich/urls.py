from django.conf.urls import url

from . import views

app_name = "enrich"

urlpatterns = [
    url(r"^$", views.SuggestionListView.as_view(), name='list'),
    url(r"^(?P<pk>\d+)/refresh/$", views.SuggestionForceLookupView.as_view(),
        name='refresh'),
    url(r"^(?P<pk>\d+)/set-wikidata-id/$", views.SetWikiDataIDView.as_view(),
        name='set_wd_id'),
]
