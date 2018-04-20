from django.conf.urls import url

from . import views

app_name = "editing_logs"

urlpatterns = [
    url(r"^$", views.LogItemListView.as_view(), name='list'),
    url(r"^movie/(?P<pk>[0-9]+)/$", views.MovieLogItemListView.as_view(),
        name='movie'),
]
