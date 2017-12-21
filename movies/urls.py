from django.conf.urls import url

from . import views

app_name = "movies"
urlpatterns = [
    url(r"^$", views.home, name='list'),
    url(r"^as-json/$", views.home_json, name='list_json'),
    url(r"^add/$", views.create, name='create'),
    url(r"^(?P<id>[0-9]+)/$", views.detail, name='detail'),
    url(r"^collections/$", views.collections_list, name='collections_list'),
]
