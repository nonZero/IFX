from django.conf.urls import url

from . import views

app_name = "people"

urlpatterns = [
    url(r"^$", views.PersonListView.as_view(), name='list'),
    url(r"^(?P<pk>[0-9]+)/$", views.PersonDetailView.as_view(), name='detail'),
]
