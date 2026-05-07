from django.contrib import admin
from .models import PaymentTransaction


@admin.register(PaymentTransaction)
class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = (
        "transaction_code",
        "booking",
        "user",
        "amount",
        "currency",
        "status",
        "provider",
        "created_at",
        "paid_at",
    )

    list_filter = ("status", "provider")

    search_fields = (
        "transaction_code",
        "provider_reference",
        "booking__id",
        "user__username",
    )

    ordering = ("-created_at",)

    readonly_fields = ("transaction_code", "paid_at", "created_at", "updated_at")