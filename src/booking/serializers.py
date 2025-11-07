from django.utils import timezone
from rest_framework import serializers

from .models import Booking, Room


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = "__all__"

    def validate(self, data):
        date_start = data.get("date_start")
        date_end = data.get("date_end")

        if date_start and date_end:
            if date_start > date_end:
                raise serializers.ValidationError(
                    "Дата окончания не может быть раньше даты начала"
                )

            if date_start < timezone.now().date():
                raise serializers.ValidationError(
                    "Нельзя бронировать на прошедшие даты"
                )

        return data
