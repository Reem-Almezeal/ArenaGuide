from django.contrib import admin
from .models import (
    ServiceCategory,
    Service,
    ServiceMenuItem,
    ServiceReview,
    Event,
)


class ServiceMenuItemInline(admin.TabularInline):
    model = ServiceMenuItem
    extra = 1


class ServiceReviewInline(admin.TabularInline):
    model = ServiceReview
    extra = 0
    readonly_fields = ("created_at",)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "display_order", "is_active")
    list_editable = ("display_order", "is_active")
    search_fields = ("name",)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "stadium", "distance", "status", "is_featured")
    search_fields = ("name", "location", "description")
    list_filter = ("status", "category", "stadium", "is_featured")
    ordering = ("category", "name")
    list_editable = ("status", "is_featured")
    inlines = [ServiceMenuItemInline, ServiceReviewInline]


@admin.register(ServiceMenuItem)
class ServiceMenuItemAdmin(admin.ModelAdmin):
    list_display = ("name", "service", "price", "is_available")
    list_filter = ("is_available", "service")
    search_fields = ("name", "service__name")


@admin.register(ServiceReview)
class ServiceReviewAdmin(admin.ModelAdmin):
    list_display = ("service", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("service__name", "user__username", "comment")
    readonly_fields = ("created_at",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("name", "stadium", "city", "start_datetime", "status", "is_featured")
    list_filter = ("status", "stadium", "city", "is_featured")
    search_fields = ("name", "city", "location")
    list_editable = ("status", "is_featured")
    filter_horizontal = ("services",)