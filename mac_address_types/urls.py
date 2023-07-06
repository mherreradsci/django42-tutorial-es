from django.urls import path
from . import views

app_name = "mac_address_types"
urlpatterns = [
    path("list/", views.MacAddressTypeListView.as_view(), name="list"),
    path("new/", views.MacAddressTypeCreateView.as_view(), name="create"),
    path("<int:pk>/", views.MacAddressTypeDetailViev.as_view(), name="detail"),
    path("<int:pk>/delete/", views.MacAddressTypeDeleteView.as_view(), name="delete"),
    path("<int:pk>/update/", views.MacAddressTypeUpdateView.as_view(), name="update"),
]
