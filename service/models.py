from django.db import models

class Service(models.Model):
    
    class Meta:
        ordering = ["-created_at"]

    stadium = models.ForeignKey("stadium.Stadium", on_delete=models.CASCADE, related_name="services")
    service_type = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=20)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def activate(self):
        self.status = "active"
        self.save()

    def deactivate(self):
        self.status = "inactive"
        self.save()

    def is_available(self):
        return self.status == "active"


class Event(models.Model):

    class Meta:
            ordering = ["-start_datetime"]

    stadium = models.ForeignKey("stadium.Stadium", on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    image = models.ImageField(upload_to="events/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    services = models.ManyToManyField("service.Service", related_name="events")

    def is_upcoming(self):
        from django.utils import timezone
        return self.start_datetime > timezone.now()

    def is_active(self):
        return self.status == "active"

    def mark_as_completed(self):
        self.status = "completed"
        self.save()

    def cancel_event(self):
        self.status = "cancelled"
        self.save()
