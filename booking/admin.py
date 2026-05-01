from django.contrib import admin
from .models import Booking, Ticket, ParkingReservation


@admin.action(description="Confirm selected bookings")
def confirm_bookings(modeladmin, request, queryset):
    for booking in queryset:
        booking.confirm_booking()


@admin.action(description="Cancel selected bookings")
def cancel_bookings(modeladmin, request, queryset):
    for booking in queryset:
        booking.cancel_booking()


@admin.action(description="Mark selected tickets as used")
def mark_tickets_as_used(modeladmin, request, queryset):
    for ticket in queryset:
        ticket.mark_as_used()


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_code",
        "user",
        "match",
        "tickets_count",
        "total_price",
        "status",
        "booked_at",
    )
    list_filter = ("status", "booked_at", "match")
    search_fields = (
        "booking_code",
        "user__username",
        "user__email",
        "match__home_team__name",
        "match__away_team__name",
    )
    ordering = ("-booked_at",)
    readonly_fields = ("booking_code", "booked_at")
    list_editable = ("status",)
    actions = [confirm_bookings, cancel_bookings]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "ticket_code",
        "booking",
        "user",
        "match",
        "seat_number",
        "gate",
        "price",
        "status",
        "issued_at",
    )
    list_filter = ("status", "match", "gate", "issued_at")
    search_fields = (
        "ticket_code",
        "booking__booking_code",
        "user__username",
        "seat_number",
    )
    ordering = ("-issued_at",)
    readonly_fields = ("ticket_code", "issued_at")
    list_editable = ("status",)
    actions = [mark_tickets_as_used]


@admin.register(ParkingReservation)
class ParkingReservationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "match",
        "stadium",
        "parking",
        "booking",
        "reservation_time",
        "status",
        "created_at",
    )
    list_filter = ("status", "stadium", "parking", "created_at")
    search_fields = (
        "user__username",
        "user__email",
        "booking__booking_code",
        "parking__name",
        "stadium__name",
    )
    ordering = ("-created_at",)
    readonly_fields = ("created_at",)
    list_editable = ("status",)