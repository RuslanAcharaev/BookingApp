from django.db import models


class Room(models.Model):
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Room #{self.pk}"


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return f"Booking #{self.pk}"
