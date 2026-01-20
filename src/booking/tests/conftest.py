from datetime import date

import pytest

from ..models import Booking, Room


@pytest.fixture
def sample_room():
    """Фикстура для тестовой комнаты"""
    return Room.objects.create(description="Стандартный номер", price=5000.00)


@pytest.fixture
def sample_booking(sample_room):
    """Фикстура для тестового бронирования"""
    return Booking.objects.create(
        room=sample_room, date_start=date(2026, 12, 15), date_end=date(2026, 12, 20)
    )
