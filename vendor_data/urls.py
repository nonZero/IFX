from django.urls import path

from . import views

app_name = "vendor_data"

urlpatterns = [
    path("", views.VendorDataListView.as_view(), name='list'),
    path("item/<int:pk>/set/movie/<int:entity_id>/",
         views.SetVendorItemEntityView.as_view(), name='set-movie'),
]
