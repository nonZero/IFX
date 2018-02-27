from django.urls import path

from . import views

app_name = "reports"

urlpatterns = [
    path("", views.ReportList.as_view(), name='list'),
]

for key, v in views.REPORTS:
    urlpatterns.append(path(key + "/", v.as_view(), name=key))
