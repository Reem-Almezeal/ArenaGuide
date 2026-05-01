from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        ORGANIZER = "organizer", "Organizer"
        IT = "it", "IT"

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SUSPENDED = "suspended", "Suspended"

    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE
    )

    def is_customer(self):
        return self.role == self.Role.CUSTOMER

    def is_organizer(self):
        return self.role == self.Role.ORGANIZER

    def is_it(self):
        return self.role == self.Role.IT

    def activate_account(self):
        self.status = self.Status.ACTIVE
        self.is_active = True
        self.save()

    def deactivate_account(self):
        self.status = self.Status.INACTIVE
        self.is_active = False
        self.save()

    def suspend_account(self):
        self.status = self.Status.SUSPENDED
        self.is_active = False
        self.save()