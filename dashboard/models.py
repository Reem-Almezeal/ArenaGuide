from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from stadium.models import Gate
from match.models import Match


class GateStatusUpdate(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"
        CROWDED = "crowded", "Crowded"
        EMERGENCY = "emergency", "Emergency"
        MAINTENANCE = "maintenance", "Maintenance"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    gate = models.ForeignKey(Gate,on_delete=models.CASCADE,related_name="status_updates")
    match = models.ForeignKey(Match,on_delete=models.CASCADE,related_name="gate_updates")
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.OPEN)
    priority = models.CharField(max_length=20,choices=Priority.choices,default=Priority.NORMAL)
    alternative_gate = models.ForeignKey(Gate,on_delete=models.SET_NULL,null=True,blank=True,related_name="alternative_status_updates")
    title = models.CharField(max_length=120, blank=True)
    message = models.TextField(blank=True,help_text="Message shown to organizers and optionally sent to visitors.")
    internal_note = models.TextField(blank=True,help_text="Private note for organizers only.")
    notify_users = models.BooleanField(default=True)
    affected_ticket_count = models.PositiveIntegerField(default=0)
    notification_sent = models.BooleanField(default=False)
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True,blank=True,related_name="gate_status_updates")
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.alternative_gate and self.alternative_gate_id == self.gate_id:
            raise ValidationError({
                "alternative_gate": "Alternative gate cannot be the same as the affected gate."
            })

        if self.status in [
            self.Status.CLOSED,
            self.Status.CROWDED,
            self.Status.EMERGENCY,
        ] and self.notify_users and not self.message:
            raise ValidationError({
                "message": "Message is required when notifying users about closed, crowded, or emergency gates."
            })

    def is_urgent(self):
        return self.priority in [self.Priority.HIGH, self.Priority.CRITICAL]

    def __str__(self):
        return f"{self.gate.name} - {self.get_status_display()} - {self.match}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Gate Status Update"
        verbose_name_plural = "Gate Status Updates"