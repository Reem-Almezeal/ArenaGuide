from django.db import models


class ContactMessage(models.Model):
    class MessageType(models.TextChoices):
        INQUIRY = "inquiry", "Inquiry"
        SUGGESTION = "suggestion", "Suggestion"
        TECHNICAL_ISSUE = "technical_issue", "Technical Issue"
        OTHER = "other", "Other"

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    message_type = models.CharField(max_length=30, choices=MessageType.choices)
    other_type = models.CharField(max_length=120, blank=True, null=True)
    subject = models.CharField(max_length=180)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.subject}"