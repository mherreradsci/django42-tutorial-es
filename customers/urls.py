from django.urls import path
from . import views

app_name = "customers"
urlpatterns = [
    path("list/", views.CustomerListView.as_view(), name="list"),
    path("new/", views.CustomerCreateView.as_view(), name="create"),
    path("<int:pk>/", views.CustomerDetailViev.as_view(), name="detail"),
    path("<int:pk>/delete/", views.CustomerDeleteView.as_view(), name="delete"),
    path("<int:pk>/update/", views.CustomerUpdateView.as_view(), name="update"),
]
