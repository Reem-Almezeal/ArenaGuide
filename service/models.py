from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError


class ServiceCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    display_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Service Category"
        verbose_name_plural = "Service Categories"

    def __str__(self):
        return self.name


class Service(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"

    stadium = models.ForeignKey(
        "stadium.Stadium",
        on_delete=models.CASCADE,
        related_name="services"
    )
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.PROTECT,
        related_name="services"
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=200)
    distance = models.FloatField(null=True, blank=True)

    delivery_apps = models.JSONField(
        blank=True,
        null=True,
        help_text="Example: ['Jahez', 'HungerStation']"
    )

    phone = models.CharField(max_length=20, blank=True)
    website_url = models.URLField(blank=True)
    opening_hours = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to="services/", null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def activate(self):
        self.status = self.Status.ACTIVE
        self.save()

    def deactivate(self):
        self.status = self.Status.INACTIVE
        self.save()

    def is_available(self):
        return self.status == self.Status.ACTIVE

    def clean(self):
        if self.distance is not None and self.distance < 0:
            raise ValidationError("Distance cannot be negative.")

    class Meta:
        ordering = ["category", "name"]
        verbose_name = "Service"
        verbose_name_plural = "Services"
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["status"]),
            models.Index(fields=["is_featured"]),
        ]

    def __str__(self):
        return f"{self.name} - {self.category.name}"


class ServiceMenuItem(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="menu_items"
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to="menu_items/", null=True, blank=True)
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["service", "name"]
        verbose_name = "Service Menu Item"
        verbose_name_plural = "Service Menu Items"

    def __str__(self):
        return f"{self.name} - {self.service.name}"


class ServiceReview(models.Model):
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="reviews"
    )
    user = models.ForeignKey(
        "account.User",
        on_delete=models.CASCADE,
        related_name="service_reviews"
    )
    rating = models.PositiveIntegerField()
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError("Rating must be between 1 and 5.")

    class Meta:
        ordering = ["-created_at"]
        unique_together = ["service", "user"]
        verbose_name = "Service Review"
        verbose_name_plural = "Service Reviews"

    def __str__(self):
        return f"{self.service.name} - {self.rating}/5"


class Event(models.Model):
    class Status(models.TextChoices):
        UPCOMING = "upcoming", "Upcoming"
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"

    stadium = models.ForeignKey(
        "stadium.Stadium",
        on_delete=models.CASCADE,
        related_name="events"
    )

    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)

    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.UPCOMING
    )

    image = models.ImageField(upload_to="events/", null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    is_featured = models.BooleanField(default=False)

    services = models.ManyToManyField(
        Service,
        blank=True,
        related_name="events"
    )

    def is_upcoming(self):
        return self.start_datetime > timezone.now()

    def is_active(self):
        return self.status == self.Status.ACTIVE

    def mark_as_completed(self):
        self.status = self.Status.COMPLETED
        self.save()

    def cancel_event(self):
        self.status = self.Status.CANCELLED
        self.save()

    class Meta:
        ordering = ["-start_datetime"]
        verbose_name = "Event"
        verbose_name_plural = "Events"

    def __str__(self):
        return self.name