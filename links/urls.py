from django.urls import path

from . import views

app_name = "links"

urlpatterns = [
    path("<ifx_entity:entity_type>/<int:entity_pk>/create/",
         views.LinkCreateView.as_view(), name='create'),
    path("<int:pk>/edit/", views.LinkUpdateView.as_view(), name='update'),
]
