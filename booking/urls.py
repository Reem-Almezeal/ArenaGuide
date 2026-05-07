from django.urls import path
from . import views

app_name = "booking"

urlpatterns = [
    path("matches/<int:match_id>/book/",views.book_ticket_page,name="book_ticket_page"),
    path("matches/<int:match_id>/booking-details/", views.booking_details, name="booking_details"),
    path("my-tickets/", views.my_tickets, name="my_tickets"),
    path("ticket/<int:ticket_id>/seat-map/", views.seat_map_page, name="seat_map"),
    path("reserve-parking/<int:ticket_id>/", views.reserve_parking, name="reserve_parking"),
    path("parking/checkout/<int:reservation_id>/", views.parking_checkout, name="parking_checkout"),
    path("parking/success/<int:reservation_id>/", views.parking_success, name="parking_success"),
    
]