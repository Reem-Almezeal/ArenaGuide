from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path( "",views.organizer_dashboard,name="organizer_dashboard"),
    path("verify-visitor/", views.verify_visitor, name="verify_visitor"),
    path("gates/",views.gate_management_view,name="gate_management_view"),
    path("gates/<int:gate_id>/update/", views.update_gate_status, name="update_gate_status"),
]