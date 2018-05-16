from django.urls import path

from . import views

app_name = "vendor_data"

urlpatterns = [
    path("", views.VendorListView.as_view(), name='list'),
    path("all/", views.VendorDataListView.as_view(), name='item_list'),
    path("<int:pk>/", views.VendorDataListView.as_view(),
         name='vendor_item_list'),
    path("item/<int:pk>/set/movie/<int:entity_id>/",
         views.SetVendorItemEntityView.as_view(), name='set-movie'),
]
