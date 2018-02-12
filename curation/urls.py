from django.conf.urls import url

from . import views

app_name = "curation"

urlpatterns = [
    url(r"^$", views.CollectionListView.as_view(), name='list'),
    url(r"^add/$", views.CollectionCreateView.as_view(), name='create'),
    url(r"^(?P<pk>[0-9]+)/$", views.CollectionDetailView.as_view(),
        name='detail'),
]
