from django.conf.urls import url

from . import views

app_name = "editing_logs"

urlpatterns = [
    url(r"^$", views.LogItemListView.as_view(), name='list'),
    # url(r"^(?P<pk>\d+)/refresh/$", views.SuggestionForceLookupView.as_view(),
    #     name='refresh'),
]
