from django.conf import settings
from django.db import models

class MenuItem(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.title} (${self.price})"

class Booking(models.Model):
    name = models.CharField(max_length=100)
    no_of_guests = models.PositiveSmallIntegerField()
    booking_date = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="bookings", null=True, blank=True
    )

    class Meta:
        ordering = ["booking_date"]

    def __str__(self):
        return f"{self.name} - {self.booking_date:%Y-%m-%d %H:%M}"
