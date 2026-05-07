from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
import uuid

class IdentityVerification(models.Model):
    class Provider(models.TextChoices):
        MANUAL = "manual", "Manual Review"
        MOCK = "mock", "Prototype Mock API"
        THIRD_PARTY = "third_party", "Third Party API"

    class Status(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        PENDING = "pending", "Pending"
        VERIFIED = "verified", "Verified"
        REJECTED = "rejected", "Rejected"

    user = models.OneToOneField("account.User",on_delete=models.CASCADE,related_name="identity_verification")
    provider = models.CharField(max_length=30, choices=Provider.choices, default=Provider.MANUAL)
    status = models.CharField(max_length=30, choices=Status.choices, default=Status.NOT_STARTED)
    id_last4 = models.CharField(max_length=4, blank=True)
    verified_full_name = models.CharField(max_length=150, blank=True)
    id_document = models.ImageField(upload_to="identity/documents/", null=True, blank=True)
    id_hash = models.CharField(max_length=64, blank=True, db_index=True)
    provider_reference = models.CharField(max_length=120, blank=True)
    admin_notes = models.TextField(blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def is_verified(self):
        return self.status == self.Status.VERIFIED

    def approve(self):
        self.status = self.Status.VERIFIED
        self.verified_at = timezone.now()
        self.save(update_fields=["status", "verified_at", "updated_at"])

    def reject(self):
        self.status = self.Status.REJECTED
        self.save(update_fields=["status", "updated_at"])

    def __str__(self):
        return f"{self.user} - {self.status}"



class SeatCategory(models.Model):
    name = models.CharField(max_length=80)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    benefits = models.TextField(blank=True)

    def __str__(self):
        return self.name




class Seat(models.Model):
    class ViewQuality(models.TextChoices):
        EXCELLENT = "excellent", "Excellent"
        GOOD = "good", "Good"
        LIMITED = "limited", "Limited"

    class SunExposure(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"

    stadium = models.ForeignKey("stadium.Stadium",on_delete=models.CASCADE,related_name="seats")
    category = models.ForeignKey(SeatCategory,on_delete=models.PROTECT,related_name="seats")
    gate = models.ForeignKey("stadium.Gate",on_delete=models.SET_NULL,null=True,blank=True,related_name="seats")
    section = models.CharField(max_length=20)
    row = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    view_quality = models.CharField(max_length=20, choices=ViewQuality.choices, default=ViewQuality.GOOD)
    is_shaded = models.BooleanField(default=False)
    sun_exposure = models.CharField(max_length=20, choices=SunExposure.choices, default=SunExposure.MEDIUM)
    notes = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def code(self):
        return f"{self.section}-{self.row}-{self.number}"

    def __str__(self):
        return f"{self.stadium.name} | {self.code}"

    class Meta:
        ordering = ["section", "row", "number"]
        constraints = [
            models.UniqueConstraint(
                fields=["stadium", "section", "row", "number"],
                name="unique_seat_per_stadium"
            )
        ]


class Booking(models.Model):
    class Status(models.TextChoices):
        PENDING_PAYMENT = "pending_payment", "Pending Payment"
        PAID = "paid", "Paid"
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"
        EXPIRED = "expired", "Expired"

    booking_code = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="bookings")
    match = models.ForeignKey("match.Match", on_delete=models.CASCADE, related_name="bookings")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    booked_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING_PAYMENT)
    identity_checked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.booking_code:
            self.booking_code = f"BKG-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)




class TicketHolder(models.Model):
    class Type(models.TextChoices):
        MR = "mr", "Mr"
        MS = "ms", "Ms"
        CHILD = "child", "Child"

    full_name = models.CharField(max_length=150)
    holder_type = models.CharField(max_length=20, choices=Type.choices)
    date_of_birth = models.DateField()
    id_last4 = models.CharField(max_length=4)
    id_hash = models.CharField(max_length=64, db_index=True)
    id_document = models.ImageField(upload_to="identity/documents/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)




class Ticket(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        USED = "used", "Used"
        CANCELLED = "cancelled", "Cancelled"

    booking = models.ForeignKey(Booking,on_delete=models.CASCADE,related_name="tickets")
    match = models.ForeignKey("match.Match",on_delete=models.CASCADE,related_name="tickets")
    user = models.ForeignKey("account.User",on_delete=models.CASCADE,related_name="tickets")
    seat = models.ForeignKey(Seat,on_delete=models.PROTECT,related_name="tickets")
    gate = models.ForeignKey("stadium.Gate",on_delete=models.SET_NULL,null=True,blank=True,related_name="tickets")
    holder = models.ForeignKey("booking.TicketHolder",on_delete=models.PROTECT,related_name="tickets",null=True,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_code = models.CharField(max_length=40, unique=True, blank=True)
    issued_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=Status.choices,default=Status.ACTIVE)

    class Meta:
        ordering = ["-issued_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["match", "seat"],
                condition=models.Q(status__in=["active", "used"]),
                name="unique_active_or_used_ticket_per_match_seat"
            ),
        ]

    def clean(self):
        errors = {}

        if self.seat and self.match:
            if self.seat.stadium_id != self.match.stadium_id:
                errors["seat"] = "Selected seat does not belong to the match stadium."

        if self.gate and self.match:
            if self.gate.stadium_id != self.match.stadium_id:
                errors["gate"] = "Selected gate does not belong to the match stadium."

        if self.seat and self.gate:
            if self.seat.gate_id and self.seat.gate_id != self.gate_id:
                errors["gate"] = "Ticket gate must match the seat gate."

        if self.price is not None and self.price < 0:
            errors["price"] = "Ticket price cannot be negative."

        if errors:
            raise ValidationError(errors)

    def generate_ticket_code(self):
        return f"TCK-{uuid.uuid4().hex[:12].upper()}"

    def save(self, *args, **kwargs):
        if not self.ticket_code:
            self.ticket_code = self.generate_ticket_code()

        if self.seat:
            self.price = self.seat.category.base_price

            if getattr(self.seat, "gate_id", None):
                self.gate = self.seat.gate

        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        return self.status == self.Status.ACTIVE

    def mark_as_used(self):
        from django.utils import timezone

        if self.status != self.Status.ACTIVE:
            raise ValidationError("Only active tickets can be marked as used.")

        self.status = self.Status.USED
        self.used_at = timezone.now()
        self.save(update_fields=["status", "used_at"])

    def cancel(self):
        if self.status == self.Status.USED:
            raise ValidationError("Used tickets cannot be cancelled.")

        self.status = self.Status.CANCELLED
        self.save(update_fields=["status"])

    def __str__(self):
        return self.ticket_code
    



class ParkingReservation(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACTIVE = "active", "Active"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey("account.User", on_delete=models.CASCADE, related_name="parking_reservations")
    match = models.ForeignKey("match.Match", on_delete=models.CASCADE, related_name="parking_reservations")
    stadium = models.ForeignKey("stadium.Stadium", on_delete=models.CASCADE, related_name="parking_reservations")
    ticket = models.OneToOneField(Ticket,on_delete=models.PROTECT,null=True,blank=True,related_name="parking_reservation")
    reservation_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def clean(self):
        if self.ticket:
            if self.ticket.user_id != self.user_id:
                raise ValidationError("Parking reservation must belong to the ticket owner.")

            if self.ticket.match_id != self.match_id:
                raise ValidationError("Parking reservation must be for the same match as the ticket.")

            if self.ticket.match.stadium_id != self.stadium_id:
                raise ValidationError("Parking reservation must be for the same stadium as the ticket.")

            if self.parking.stadium_id != self.stadium_id:
                raise ValidationError("Parking must belong to the selected stadium.")

    def reserve_spot(self):
        if self.parking.is_available():
            self.parking.reserve_spot()
            self.status = self.Status.PENDING
            self.save()

    def confirm_payment(self):
        self.paid = True
        self.status = self.Status.ACTIVE
        self.save(update_fields=["paid", "status"])

    def cancel_reservation(self):
        self.status = self.Status.CANCELLED
        self.parking.release_spot()
        self.save(update_fields=["status"])

    def is_active(self):
        return self.status == self.Status.ACTIVE

    def __str__(self):
        return f"{self.user} - {self.parking}"

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "match"],
                condition=models.Q(status="active"),
                name="unique_active_parking_per_user_match"
            ),
            models.UniqueConstraint(
                fields=["ticket"],
                condition=models.Q(status__in=["pending", "active"]),
                name="unique_parking_per_active_ticket"
            )
        ]