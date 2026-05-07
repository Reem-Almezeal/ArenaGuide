from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import logout
from django.http import HttpRequest,HttpResponse

User = get_user_model()


def register_view(request:HttpRequest):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.Role.CUSTOMER
            user.status = User.Status.ACTIVE
            user.set_password(form.cleaned_data["password"])
            user.save()

            messages.success(request, "Account created successfully. Please login.")
            return redirect("account:login")
        messages.error(request, "Please fix the errors below.")

    else:
        form = RegisterForm()
    return render(request, "account/register.html", {"form": form})


def login_view(request:HttpRequest):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()

            if user.status != User.Status.ACTIVE:
                messages.error(request, "Your account is not active.")
                return redirect("account:login")

            login(request, user)
            messages.success(request, "Logged in successfully.")

            if user.is_customer():
                return redirect("core:home")

            if user.is_organizer():
                return redirect("account:organizer_dashboard")

            if user.is_it():
                return redirect("account:it_dashboard")
            return redirect("account:profile")
        messages.error(request, "Invalid username or password.")

    else:
        form = LoginForm()
    return render(request, "account/login.html", {"form": form})


@login_required(login_url="account:login")
def profile_view(request:HttpRequest):
    if request.user.status != User.Status.ACTIVE:
        messages.error(request, "Your account is not active.")
        return redirect("account:login")
    return render(request, "account/profile.html")


@login_required(login_url="account:login")
def organizer_dashboard_view(request:HttpRequest):
    if not request.user.is_organizer():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("core:home")
    return render(request, "account/organizer_dashboard.html")


@login_required(login_url="account:login")
def it_dashboard_view(request:HttpRequest):
    if not request.user.is_it():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("core:home")

    return render(request, "account/it_dashboard.html")


@login_required
def logout_view(request:HttpRequest):
    if request.method == "POST":
        logout(request)
        messages.success(request, "Logged out successfully.")
    return redirect("core:home")

@login_required
def profile_view(request):
    return render(request, "account/profile.html")