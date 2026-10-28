from django.db import models


class Menu(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField(default=0)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return f"{self.title} : {self.price}"


class Booking(models.Model):
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField()
    booking_date = models.DateTimeField()

    class Meta:
        ordering = ["booking_date"]

    def __str__(self):
        return f"{self.name} - {self.booking_date:%Y-%m-%d %H:%M}"
