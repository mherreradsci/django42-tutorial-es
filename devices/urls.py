from django.urls import path
from . import views

app_name = "devices"
urlpatterns = [
    # path("", views.index, name="device-index"),
    path("list", views.DeviceListView.as_view(), name="list"),
    path("new", views.DeviceCreateView.as_view(), name="create"),
    path("<int:pk>", views.DeviceDetailViev.as_view(), name="detail"),
    path("<int:pk>/delete", views.DeviceDeleteView.as_view(), name="delete"),
    path("<int:pk>/update", views.DeviceUpdateView.as_view(), name="update"),
]
