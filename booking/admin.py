from django.contrib import admin
from .models import (IdentityVerification,SeatCategory,Seat,Booking,Ticket,ParkingReservation,)


@admin.action(description="Approve selected identity verifications")
def approve_identity(modeladmin, request, queryset):
    for item in queryset:
        item.approve()


@admin.action(description="Reject selected identity verifications")
def reject_identity(modeladmin, request, queryset):
    for item in queryset:
        item.reject()


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


@admin.register(IdentityVerification)
class IdentityVerificationAdmin(admin.ModelAdmin):
    list_display = ("user","provider","status","id_last4","verified_full_name","verified_at","updated_at",)
    list_filter = ("provider", "status", "verified_at")
    search_fields = ("user__username","user__email","verified_full_name","provider_reference",)
    readonly_fields = ("verified_at", "created_at", "updated_at")
    list_editable = ("status",)
    actions = [approve_identity, reject_identity]


@admin.register(SeatCategory)
class SeatCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "base_price")
    search_fields = ("name",)


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ("code","stadium","category","gate","view_quality","is_shaded","sun_exposure","is_active",)
    list_filter = ("stadium","category","gate","view_quality","is_shaded","sun_exposure","is_active",)
    search_fields = ("section", "row", "number", "stadium__name")
    list_editable = ("is_active",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("booking_code","user","match","total_price","status","identity_checked","booked_at",)
    list_filter = ("status", "identity_checked", "booked_at", "match")
    search_fields = ("booking_code","user__username","user__email","match__home_team__name","match__away_team__name","seat__section","seat__row","seat__number",)
    ordering = ("-booked_at",)
    readonly_fields = ("booking_code", "booked_at")
    list_editable = ("status",)
    actions = [confirm_bookings, cancel_bookings]


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("ticket_code","booking","user","match","seat","gate","price","status","issued_at",)
    list_filter = ("status", "match", "gate", "issued_at")
    search_fields = ("ticket_code","booking__booking_code","user__username","user__email","seat__section","seat__row","seat__number",)
    ordering = ("-issued_at",)
    readonly_fields = ("ticket_code", "issued_at")
    list_editable = ("status",)
    actions = [mark_tickets_as_used]


@admin.register(ParkingReservation)
class ParkingReservationAdmin(admin.ModelAdmin):
    list_display = ("user","match","stadium","ticket","reservation_time","price","paid","status","created_at",)
    list_filter = ("status","paid","stadium","created_at",)
    search_fields = ( "user__username", "user__email", "ticket__ticket_code", "parking__name", "stadium__name", "match__home_team__name", "match__away_team__name")
    ordering = ("-created_at",)
    readonly_fields = ( "created_at",)
    list_editable = ("status","paid",)