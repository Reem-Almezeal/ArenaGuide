from django.contrib import admin
from .models import GateStatusUpdate


@admin.register(GateStatusUpdate)
class GateStatusUpdateAdmin(admin.ModelAdmin):
    list_display = ("gate","match","status","priority","alternative_gate","notify_users","notification_sent","affected_ticket_count","updated_by","created_at",)
    list_filter = ("status","priority","notify_users","notification_sent","match","created_at",)
    search_fields = ( "gate__name", "alternative_gate__name", "match__home_team__name", "match__away_team__name", "match__stadium__name", "title", "message", "updated_by__username", "updated_by__email",)
    readonly_fields = ("created_at","notification_sent", "affected_ticket_count",)
    list_editable = ( "status", "priority", "notify_users",)
    fieldsets = ((
            "Gate & Match",
            {
                "fields": (
                    "match",
                    "gate",
                    "alternative_gate",
                )
            },
        ),
        (
            "Status Update",
            {
                "fields": (
                    "status",
                    "priority",
                    "title",
                    "message",
                    "internal_note",
                )
            },
        ),
        (
            "Notification Settings",
            {
                "fields": (
                    "notify_users",
                    "notification_sent",
                    "affected_ticket_count",
                )
            },
        ),
        (
            "Tracking",
            {
                "fields": (
                    "updated_by",
                    "created_at",
                )
            },
        ),
    )

    ordering = ("-created_at",)

    def save_model(self, request, obj, form, change):
        if not obj.updated_by:
            obj.updated_by = request.user
        super().save_model(request, obj, form, change)