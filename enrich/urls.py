from django.conf.urls import url

from . import views

app_name = "enrich"

urlpatterns = [
    url(r"^$", views.SuggestionListView.as_view(), name='list'),
]
