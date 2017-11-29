from django.conf.urls import url

from . import views

app_name = "movies"
urlpatterns = [
    url(r"^$", views.home, name='list'),
    url(r"^(?P<id>[0-9]+)/$", views.detail, name='detail'),
]
