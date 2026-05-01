from django.db import models
from django.utils import timezone
import uuid

class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    booking_code = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="bookings")
    match = models.ForeignKey("match.Match", on_delete=models.CASCADE, related_name="bookings")
    tickets_count = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booked_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = f"BKG-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def is_confirmed(self):
        return self.status == self.Status.CONFIRMED

    def confirm_booking(self):
        self.status = self.Status.CONFIRMED
        self.save()

    def cancel_booking(self):
        self.status = self.Status.CANCELLED
        self.save()

    def calculate_total_price(self):
        return self.total_price

    class Meta:
        ordering = ["-booked_at"]

    def __str__(self):
        return self.booking_code


class Ticket(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        USED = "used", "Used"
        CANCELLED = "cancelled", "Cancelled"

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="tickets")
    match = models.ForeignKey("match.Match", on_delete=models.CASCADE, related_name="tickets")
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="tickets")
    seat_number = models.CharField(max_length=20)
    gate = models.ForeignKey("stadium.Gate", on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_code = models.CharField(max_length=30, unique=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    def generate_ticket_code(self):
        return f"TCK-{uuid.uuid4().hex[:10].upper()}"

    def save(self, *args, **kwargs):
        if not self.ticket_code:
            self.ticket_code = self.generate_ticket_code()
        super().save(*args, **kwargs)

    def mark_as_used(self):
        self.status = self.Status.USED
        self.save()

    def is_valid(self):
        return self.status == self.Status.ACTIVE

    class Meta:
        ordering = ["-issued_at"]
        unique_together = ["match", "seat_number"]

    def __str__(self):
        return self.ticket_code


class ParkingReservation(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey("account.User", on_delete=models.CASCADE)
    match = models.ForeignKey("match.Match", on_delete=models.CASCADE)
    stadium = models.ForeignKey("stadium.Stadium", on_delete=models.CASCADE)
    parking = models.ForeignKey("stadium.Parking", on_delete=models.CASCADE)

    booking = models.ForeignKey(
        Booking,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="parking_reservations"
    )

    reservation_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    def reserve_spot(self):
        if self.parking.is_available():
            self.parking.reserve_spot()
            self.save()

    def cancel_reservation(self):
        self.status = self.Status.CANCELLED
        self.parking.release_spot()
        self.save()

    def is_active(self):
        return self.status == self.Status.ACTIVE

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user} - {self.parking}"