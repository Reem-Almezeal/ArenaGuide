from django.contrib import admin
from .models import ContactMessage


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "message_type", "subject", "is_read", "created_at")
    list_filter = ("message_type", "is_read", "created_at")
    search_fields = ("name", "email", "subject", "message", "other_type")
    readonly_fields = ("name", "email", "phone", "message_type", "other_type", "subject", "message", "created_at")