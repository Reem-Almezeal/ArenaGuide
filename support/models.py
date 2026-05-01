from django.db import models


class SupportTicket(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        CLOSED = "closed", "Closed"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="support_tickets"
    )

    subject = models.CharField(max_length=255)
    message = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    priority = models.CharField(
        max_length=20,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def mark_as_open(self):
        self.status = self.Status.OPEN
        self.save()

    def mark_as_progress(self):
        self.status = self.Status.IN_PROGRESS
        self.save()

    def close_ticket(self):
        self.status = self.Status.CLOSED
        self.save()

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Support Ticket"
        verbose_name_plural = "Support Tickets"

    def __str__(self):
        return self.subject


class Reply(models.Model):
    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name="replies"
    )

    sender = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="support_replies"
    )

    message = models.TextField()
    is_internal = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_staff_reply(self):
        return self.sender.is_it() or self.sender.is_organizer()

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Reply"
        verbose_name_plural = "Replies"

    def __str__(self):
        return f"Reply by {self.sender}"