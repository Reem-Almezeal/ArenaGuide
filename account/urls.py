from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path

from . import views

app_name = "account"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", LogoutView.as_view(next_page="core:home"), name="logout"),
    path("profile/", views.profile_view, name="profile"),
    path("organizer-dashboard/", views.organizer_dashboard_view, name="organizer_dashboard"),
    path("it-dashboard/", views.it_dashboard_view, name="it_dashboard"),
    path("password-reset/",auth_views.PasswordResetView.as_view( template_name="account/forgot_password.html",email_template_name="account/password_reset_email.html",success_url="/account/password-reset/done/",),name="password_reset",),
    path("password-reset/done/",auth_views.PasswordResetDoneView.as_view(template_name="account/password_reset_done.html",),name="password_reset_done",),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(template_name="account/password_reset.html",success_url="/account/reset/done/",),name="password_reset_confirm",),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(template_name="account/password_reset_complete.html",),name="password_reset_complete",),
]