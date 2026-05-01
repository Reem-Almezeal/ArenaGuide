from django.db import models


class Stadium(models.Model):

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Stadium"
        verbose_name_plural = "Stadiums"
        unique_together = ["name", "city"]

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        MAINTENANCE = "maintenance", "Maintenance"

    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    capacity = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="stadiums/", blank=True, null=True)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_available(self):
        return self.status == self.Status.ACTIVE

    def update_status(self, status):
        self.status = status
        self.save()

    def __str__(self):
        return self.name
    

class Gate(models.Model):

    class Meta:
        ordering = ["name"]
        verbose_name = "Gate"
        verbose_name_plural = "Gates"
        unique_together = ["stadium", "name"]

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"
        MAINTENANCE = "maintenance", "Maintenance"

    stadium = models.ForeignKey("Stadium",on_delete=models.CASCADE,related_name="gates")
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.CLOSED)

    def open_gate(self):
        self.status = self.Status.OPEN
        self.save()

    def close_gate(self):
        self.status = self.Status.CLOSED
        self.save()

    def is_open(self):
        return self.status == self.Status.OPEN

    def __str__(self):
        return f"{self.name} - {self.stadium.name}"


class Parking(models.Model):

    class Meta:
        ordering = ["name"]
        verbose_name = "Parking"
        verbose_name_plural = "Parkings"
        unique_together = ["stadium", "name"]

    class Status(models.TextChoices):
        AVAILABLE = "available", "Available"
        FULL = "full", "Full"
        CLOSED = "closed", "Closed"

    stadium = models.ForeignKey("Stadium",on_delete=models.CASCADE,related_name="parkings")
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=255)
    capacity_spots = models.PositiveIntegerField()
    available_spots = models.PositiveIntegerField()
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.AVAILABLE
    )

    def is_available(self):
        return self.status == self.Status.AVAILABLE and self.available_spots > 0

    def reserve_spot(self, count=1):
        if self.available_spots >= count:
            self.available_spots -= count
            if self.available_spots == 0:
                self.status = self.Status.FULL
            self.save()

    def release_spot(self, count=1):
        self.available_spots = min(self.available_spots + count, self.capacity_spots)
        if self.available_spots > 0:
            self.status = self.Status.AVAILABLE
        self.save()

    def __str__(self):
        return f"{self.name} - {self.stadium.name}"


class Facility(models.Model):
    class Meta:
        unique_together = ["stadium", "name"]
        
    stadium = models.ForeignKey("stadium.Stadium", on_delete=models.CASCADE, related_name="facilities")
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=50)
    location = models.CharField(max_length=200)
    x_coordinate = models.FloatField()
    y_coordinate = models.FloatField()
    status = models.CharField(max_length=20)

    def is_available(self):
        return self.status == "available"
    def update_status(self, status):
        self.status = status
        self.save()
