import pytest
from rest_framework import status


@pytest.mark.django_db(transaction=True)
class TestRoomAPI:
    def test_list_rooms(self, client, sample_room):
        """Тест получения списка комнат"""
        response = client.get("/api/rooms/")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["description"] == sample_room.description

    def test_create_room(self, client):
        """Тест создания комнаты"""
        data = {"description": "Новый номер", "price": "7500.00"}
        response = client.post(
            "/api/rooms/", data=data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["description"] == "Новый номер"


@pytest.mark.django_db(transaction=True)
class TestBookingAPI:
    def test_list_bookings_with_room_filter(self, client, sample_booking, sample_room):
        """Тест фильтрации бронирований по room_id"""
        response = client.get(f"/api/bookings/?room_id={sample_room.id}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["room"] == sample_room.id

    def test_create_booking_conflict(self, client, sample_room, sample_booking):
        """Тест создания бронирования c конфликтом дат"""
        data = {
            "room": sample_room.id,
            "date_start": "2026-12-18",  # пересекается c существующим
            "date_end": "2026-12-22",
        }
        response = client.post(
            "/api/bookings/", data=data, content_type="application/json"
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "room" in response.data  # Ошибка должна быть связана c полем room
