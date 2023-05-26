from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.conf import settings


# Create your views here.
def login_view(request):
    if not request.user.is_authenticated:
        return redirect(f"{settings.LOGIN_URL}?next={request.path}")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("customers:list")
    else:
        form = AuthenticationForm(request)
    context = {"form": form}
    return render(request, "accounts/login.html", context)


def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("accounts:login")
    return render(request, "accounts/logout.html", {})


def register_view(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        user_obj = form.save()
        return redirect("accounts:login")
    context = {"form": form}
    return render(request, "accounts/register.html", context)
