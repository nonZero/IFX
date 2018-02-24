from django.conf.urls import url

from . import views

app_name = "links"

urlpatterns = [
    url(r"^movie/(?P<parent_pk>[0-9]+)/create/$",
        views.MovieLinkCreateView.as_view(),
        name='create_movie'),
    url(r"^people/(?P<parent_pk>[0-9]+)/create/$",
        views.PersonLinkCreateView.as_view(),
        name='create_person'),
]
