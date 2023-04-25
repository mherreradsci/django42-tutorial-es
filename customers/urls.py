from django.urls import path
from . import views

app_name = "customers"
urlpatterns = [
    path("", views.index, name="customer-index"),
    # path("list", views.customer_list, name="customer-list"),
    path("list", views.CustomerListView.as_view(), name="customer-list"),
    # path("new", views.customer_create, name="customer-create"),
    path("new", views.CustomerCreateView.as_view(), name="customer-create"),
    # path("<int:pk>", views.customer_detail, name="customer-detail"),
    path("<int:pk>", views.CustomerDetailViev.as_view(), name="customer-detail"),
    # path("<int:pk>/delete", views.customer_delete, name="customer-delete"),
    path("<int:pk>/delete", views.CustomerDeleteView.as_view(), name="customer-delete"),
    # path("<int:pk>/update", views.customer_update, name="customer-update"),
    path("<int:pk>/update", views.CustomerUpdateView.as_view(), name="customer-update"),
]
