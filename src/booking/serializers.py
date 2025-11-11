from django.utils import timezone
from rest_framework import serializers

from .models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"

    def validate(self, data):
        price = data.get("price")

        if price:
            if price < 0:
                raise serializers.ValidationError(
                    {"price": "Цена не может быть отрицательной"}
                )
        return data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    def validate(self, data):
        date_start = data.get("date_start")
        date_end = data.get("date_end")
        room = data.get("room")

        if date_start and date_end and room:
            if date_start > date_end:
                raise serializers.ValidationError(
                    {"date_start": "Дата окончания не может быть раньше даты начала"}
                )

            if date_start < timezone.now().date():
                raise serializers.ValidationError(
                    {"date_start": "Нельзя бронировать на прошедшие даты"}
                )

        overlapping_bookings = Booking.objects.filter(
            room=room, date_start__lte=date_end, date_end__gte=date_start
        )

        if self.instance and self.instance.pk:
            overlapping_bookings = overlapping_bookings.exclude(pk=self.instance.pk)

        if overlapping_bookings.exists():
            raise serializers.ValidationError(
                {"room": "Комната уже забронирована на указанные даты"}
            )

        return data
