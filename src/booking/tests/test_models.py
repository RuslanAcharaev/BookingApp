from datetime import date

import pytest

from ..models import Booking, Room


@pytest.mark.django_db(transaction=True)
class TestRoomModel:
    def test_room_creation(self):
        """Тест создания комнаты"""
        room = Room.objects.create(description="Тестовый номер", price=5000.00)
        assert room.description == "Тестовый номер"
        assert room.price == 5000.00
        assert str(room) == f"Room #{room.pk}"


@pytest.mark.django_db(transaction=True)
class TestBookingModel:
    def test_booking_creation(self):
        """Тест создания бронирования"""
        room = Room.objects.create(description="Номер", price=5000.00)
        booking = Booking.objects.create(
            room=room, date_start=date(2026, 12, 15), date_end=date(2026, 12, 20)
        )
        assert booking.room == room
        assert str(booking) == f"Booking #{booking.pk}"


@pytest.mark.django_db(transaction=True)
class TestBookingWithFixtures:
    def test_booking_relationships(self, sample_booking, sample_room):
        """Тест связей бронирования c комнатой"""
        assert sample_booking.room == sample_room
        assert sample_booking in sample_room.booking_set.all()
