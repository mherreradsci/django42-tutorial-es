from django.urls import path
from . import views
app_name = "customers"
urlpatterns = [
    path('', views.index, name='customer-index'),
    path('list', views.customer_list, name='customer-list'),
    path('new', views.customer_create, name='customer-create'),
    path('<int:pk>', views.customer_detail, name='customer-detail'),
    path('<int:pk>/delete', views.customer_delete, name='customer-delete'),
    path('<int:pk>/update', views.customer_update, name='customer-update'),
]
