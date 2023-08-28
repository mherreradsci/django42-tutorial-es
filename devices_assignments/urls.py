from django.urls import path
from devices_assignments import views

app_name = "devices_assignments"
urlpatterns = [
    # path("<int:customer_pk>/", views.CustomerCreateView.as_view(), name="create"),
    # path("list/", views.DeviceListView.as_view(), name="list"),
    # path("<int:pk>/", views.DeviceDetailViev.as_view(), name="detail"),
    # path("<int:pk>/delete/", views.DeviceDeleteView.as_view(), name="delete"),
    path("<int:pk>/", views.CustomerUpdateView.as_view(), name="update"),
]
