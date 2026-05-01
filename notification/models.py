from django.db import models


class Notification(models.Model):

    class Type(models.TextChoices):
        BOOKING = "booking", "Booking"
        MATCH = "match", "Match"
        PAYMENT = "payment", "Payment"
        SUPPORT = "support", "Support"
        SYSTEM = "system", "System"

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    sender = models.ForeignKey(
        "account.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sent_notifications"
    )

    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=Type.choices, default=Type.SYSTEM)
    link = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def mark_as_read(self):
        self.is_read = True
        self.save()

    def mark_as_unread(self):
        self.is_read = False
        self.save()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title