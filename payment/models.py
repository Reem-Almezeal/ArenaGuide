from django.db import models
from django.utils import timezone
import uuid


class PaymentTransaction(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCESS = "success", "Success"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    class Provider(models.TextChoices):
        PROTOTYPE = "prototype", "Prototype Payment"
        STRIPE = "stripe", "Stripe"
        MOYASAR = "moyasar", "Moyasar"
        HYPERPAY = "hyperpay", "HyperPay"

    transaction_code = models.CharField(max_length=30, unique=True, blank=True)
    booking = models.OneToOneField("booking.Booking",on_delete=models.CASCADE,related_name="payment_transaction")
    user = models.ForeignKey("account.User",on_delete=models.CASCADE,related_name="payment_transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default="SAR")
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.PENDING)
    provider = models.CharField(max_length=30,choices=Provider.choices,default=Provider.PROTOTYPE)
    provider_reference = models.CharField(max_length=120, blank=True)
    failure_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def generate_transaction_code(self):
        return f"PAY-{uuid.uuid4().hex[:10].upper()}"

    def mark_as_success(self, provider_reference=""):
        self.status = self.Status.SUCCESS
        self.provider_reference = provider_reference
        self.paid_at = timezone.now()
        self.save(update_fields=["status", "provider_reference", "paid_at", "updated_at"])

    def mark_as_failed(self, reason=""):
        self.status = self.Status.FAILED
        self.failure_reason = reason
        self.save(update_fields=["status", "failure_reason", "updated_at"])

    def save(self, *args, **kwargs):
        if not self.transaction_code:
            self.transaction_code = self.generate_transaction_code()

        super().save(*args, **kwargs)

    def __str__(self):
        return self.transaction_code