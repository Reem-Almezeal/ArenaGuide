from django.urls import path
from . import views

app_name = "payment"

urlpatterns = [
    path("checkout/<int:booking_id>/", views.checkout, name="checkout"),
    path("success/<int:booking_id>/", views.payment_success, name="payment_success"),
]