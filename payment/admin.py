from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("booking", "amount", "payment_method", "payment_status", "paid_at")
    list_filter = ("payment_status", "payment_method", "paid_at")
    search_fields = ("booking__booking_code", "transaction_id")
    ordering = ("-paid_at",)
    readonly_fields = ("transaction_id", "paid_at")