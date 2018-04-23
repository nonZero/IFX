from django.conf.urls import url

from movies.models import Movie
from people.models import Person
from . import views

app_name = "editing_logs"

urlpatterns = [
    url(r"^$", views.LogItemListView.as_view(), name='list'),
    url(r"^movie/(?P<pk>[0-9]+)/$", views.EntityLogItemListView.as_view(),
        kwargs={'model': Movie},
        name='movie'),
    url(r"^person/(?P<pk>[0-9]+)/$", views.EntityLogItemListView.as_view(),
        kwargs={'model': Person},
        name='person'),
]
