from django.contrib import admin
from .models import Stadium, Gate, Parking, Facility


@admin.register(Stadium)
class StadiumAdmin(admin.ModelAdmin):
    list_display = ("name", "city", "capacity", "status", "created_at")
    list_filter = ("status", "city")
    search_fields = ("name", "city", "location")
    ordering = ("name",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(Gate)
class GateAdmin(admin.ModelAdmin):
    list_display = ("name", "stadium", "status")
    list_filter = ("status", "stadium")
    search_fields = ("name", "stadium__name")
    ordering = ("stadium", "name")
    list_editable = ("status",)


@admin.register(Parking)
class ParkingAdmin(admin.ModelAdmin):
    list_display = ("name", "stadium", "capacity_spots", "available_spots", "status")
    list_filter = ("status", "stadium")
    search_fields = ("name", "location", "stadium__name")
    ordering = ("stadium", "name")
    list_editable = ("status", "available_spots")


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ("name", "stadium", "type", "status")
    list_filter = ("status", "type", "stadium")
    search_fields = ("name", "type", "location", "stadium__name")
    ordering = ("stadium", "name")
    list_editable = ("status",)

