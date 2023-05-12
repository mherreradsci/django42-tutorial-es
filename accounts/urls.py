from django.urls import path
from . import views

from django.contrib.auth import views as auth_views
from .forms import CustomAuthForm

app_name = "accounts"
urlpatterns = [
    # path('login/', views.login_view, name="login"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="accounts/login.html", authentication_form=CustomAuthForm
        ),
        name="login",
        kwargs={"authentication_form": CustomAuthForm},
    ),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
]
