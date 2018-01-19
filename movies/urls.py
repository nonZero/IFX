from django.conf.urls import url

from . import views

app_name = "movies"
urlpatterns = [

    url(r"^$", views.HomePage.as_view(), name='home'),

    url(r"^movies/$", views.MovieListView.as_view(), name='movies_list'),
    url(r"^movies/search/$", views.MoviesSearchListView.as_view(), name='search_query'),

    url(r"^tag/$", views.TagListView.as_view(), name='tag_list'),

    url(r"^movies/as-json/$", views.movies_json, name='movies_list_json'),
    url(r"^movies/add/$", views.movie_create, name='movie_create'),
    url(r"^movies/(?P<id>[0-9]+)/$", views.movie_detail, name='movie_detail'),
    url(r"^movies/collections/$", views.collections_list, name='collections_list'),
    url(r"^movies/collections/add/$", views.collection_create, name='collection_create'),
    url(r"^movies/collections/(?P<id>[0-9]+)/$", views.collection_detail, name='collection_detail'),
    url(r"^movies/about/$", views.about, name='about'),
    #url(r"^searchresult/$", views.MoviesSearchListView.as_view(), name='searchresult'),
    url(r"^movies/searchresult/$", views.searchresult, name='searchresult'),
    url(r"^movies/movie_details/$", views.movie_details, name='movie_details'),
    url(r"^movies/search/year/$", views.search_by_year, name='search_by_year'),
    url(r"^field/$", views.field_list, name='field_list'),
    url(r"^field/(?P<id>[0-9]+)/$", views.field_detail, name='field_detail'),
    url(r"^tag/(?P<id>[0-9]+)/$", views.tag_detail, name='tag_detail'),
    url(r"^person/$", views.person_list, name='person_list'),
    url(r"^person/(?P<id>[0-9]+)/$", views.person_detail, name='person_detail'),
]
