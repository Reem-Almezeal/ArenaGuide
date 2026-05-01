from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.action(description="Activate selected users")
def activate_users(modeladmin, request, queryset):
    for user in queryset:
        user.activate_account()


@admin.action(description="Deactivate selected users")
def deactivate_users(modeladmin, request, queryset):
    for user in queryset:
        user.deactivate_account()


@admin.action(description="Suspend selected users")
def suspend_users(modeladmin, request, queryset):
    for user in queryset:
        user.suspend_account()


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "status", "is_active")
    list_filter = ("role", "status", "is_active")
    search_fields = ("username", "email", "phone")
    ordering = ("username",)
    list_editable = ("role", "status", "is_active")
    actions = [activate_users, deactivate_users, suspend_users]

    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {
            "fields": ("phone", "role", "status"),
        }),
    )