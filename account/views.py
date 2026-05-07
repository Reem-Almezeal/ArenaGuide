from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
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

def login_view(request: HttpRequest):
    if request.user.is_authenticated:
        return redirect("core:home")

    if request.method == "POST":
        email = request.POST.get("username")  # لأن الفورم اسم الحقل username
        password = request.POST.get("password")

        user_obj = User.objects.filter(email=email).first()

        if user_obj is not None:
            user = authenticate(request, username=user_obj.username, password=password)

            if user is not None:
                if user.status != User.Status.ACTIVE:
                    messages.error(request, "Your account is not active.")
                    return redirect("account:login")

                login(request, user)
                messages.success(request, "Logged in successfully.")

                if user.is_customer():
                    return redirect("core:home")

                if user.is_organizer():
                    return redirect("dashboard:organizer_dashboard")

                if user.is_it():
                    return redirect("dashboard:it_dashboard")

                return redirect("account:profile")

        messages.error(request, "Invalid email or password.")

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
    return render(request, "dashboard/organizer_dashboard.html")


@login_required(login_url="account:login")
def it_dashboard_view(request:HttpRequest):
    if not request.user.is_it():
        messages.error(request, "You do not have permission to access this page.")
        return redirect("core:home")

    return render(request, "dashboard/organizer_dashboard.html")


@login_required(login_url="account:login")
def logout_view(request: HttpRequest):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect("core:home")

