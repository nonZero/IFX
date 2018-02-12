from django.conf.urls import url

import people.views
import search.views
from . import views

app_name = "movies"
urlpatterns = [

    url(r"^$", views.HomePage.as_view(), name='home'),

    url(r"^about/$", views.AboutView.as_view(), name='about'),

    url(r"^movie/$", views.MovieListView.as_view(), name='list'),
    url(r"^movie/(?P<pk>[0-9]+)/$", views.MovieDetailView.as_view(),
        name='detail'),

    url(r"^field/$", views.FieldListView.as_view(), name='field_list'),
    url(r"^field/(?P<pk>[0-9]+)/$", views.FieldDetailView.as_view(),
        name='field_detail'),
    url(r"^tag/$", views.TagListView.as_view(), name='tag_list'),
    url(r"^tag/(?P<pk>[0-9]+)/$", views.TagDetailView.as_view(), name='tag_detail'),

]
