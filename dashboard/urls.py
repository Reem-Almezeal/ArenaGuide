from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path( "",views.organizer_dashboard,name="organizer_dashboard"),
    path("verify-visitor/", views.verify_visitor, name="verify_visitor"),
    

]