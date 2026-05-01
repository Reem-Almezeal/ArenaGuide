from django.contrib import admin
from .models import SupportTicket, Reply


@admin.action(description="Close selected tickets")
def close_tickets(modeladmin, request, queryset):
    queryset.update(status=SupportTicket.Status.CLOSED)


@admin.action(description="Mark selected tickets as In Progress")
def mark_as_in_progress(modeladmin, request, queryset):
    queryset.update(status=SupportTicket.Status.IN_PROGRESS)


@admin.action(description="Mark selected tickets as Open")
def mark_as_open(modeladmin, request, queryset):
    queryset.update(status=SupportTicket.Status.OPEN)


class ReplyInline(admin.TabularInline):
    model = Reply
    extra = 1
    fields = ("sender", "message", "is_internal", "created_at")
    readonly_fields = ("created_at",)


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "status", "priority", "created_at")
    list_filter = ("status", "priority", "created_at")
    search_fields = ("subject", "message", "user__username", "user__email")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")
    list_editable = ("status", "priority")
    inlines = [ReplyInline]
    actions = [close_tickets, mark_as_in_progress, mark_as_open]


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    list_display = ("ticket", "sender", "is_internal", "created_at")
    list_filter = ("is_internal", "created_at")
    search_fields = ("message", "sender__username", "ticket__subject")
    ordering = ("created_at",)
    readonly_fields = ("created_at", "updated_at")
