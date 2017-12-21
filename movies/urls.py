from django.conf.urls import url

from . import views

app_name = "movies"
urlpatterns = [
    url(r"^movies/$", views.movies_list, name='movies_list'),
    url(r"^movies/as-json/$", views.movies_json, name='movies_list_json'),
    url(r"^movies/add/$", views.movie_create, name='movie_create'),
    url(r"^movies/(?P<id>[0-9]+)/$", views.movie_detail, name='movie_detail'),
    url(r"^collections/$", views.collections_list, name='collections_list'),
]
