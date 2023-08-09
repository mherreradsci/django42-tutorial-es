from .forms import CustomAuthForm, CustomUserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect


def login_view(request):
    if request.method == "POST":
        form = CustomAuthForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if "next" in request.POST:
                return redirect(request.POST.get("next"))
            else:
                return redirect("customers:list")
    else:
        form = CustomAuthForm(request)
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
