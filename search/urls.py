from django.conf.urls import url

from . import views

app_name = "search"
urlpatterns = [
    url(r"^$", views.MoviesSearchListView.as_view(), name='query'),

    # #url(r"^searchresult/$", views.MoviesSearchListView.as_view(), name='searchresult'),
    # url(r"^$", search.views.searchresult, name='searchresult'),
    # url(r"^by-year/$", views.search_by_year, name='search_by_year'),
]
