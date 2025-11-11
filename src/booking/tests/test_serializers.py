import pytest

from ..serializers import BookingSerializer, RoomSerializer


class TestRoomSerializer:
    @pytest.mark.parametrize(
        "description,price,should_be_valid",
        [
            # Валидные данные
            ("Стандартный номер", "5000.00", True),
            ("Люкс c видом на море", "15000.50", True),
            ("Эконом", "1000", True),  # без копеек
            ("H" * 255, "9999999.99", True),  # максимальная длина описания
            # Невалидные данные
            ("", "5000.00", False),  # пустое описание
            ("Номер", "", False),  # пустая цена
            ("Номер", "-1000.00", False),  # отрицательная цена
            ("Номер", "100000000.00", False),  # превышение max_digits=10
            ("Номер", "1000.123", False),  # больше 2 decimal_places
            ("H" * 256, "5000.00", False),  # превышение max_length=255
        ],
    )
    @pytest.mark.django_db(transaction=True)
    def test_room_field_validation(self, description, price, should_be_valid):
        """Тест валидации полей комнаты"""
        data = {"description": description, "price": price}
        serializer = RoomSerializer(data=data)
        assert serializer.is_valid() == should_be_valid

        if not should_be_valid:
            # Проверяем, что есть ожидаемые ошибки
            assert len(serializer.errors) > 0


class TestBookingSerializer:
    @pytest.mark.parametrize(
        "room_id,date_start,date_end,should_be_valid,expected_error_field",
        [
            # Валидные данные
            (1, "2026-12-15", "2026-12-20", True, None),
            # Невалидные форматы дат
            (1, "invalid-date", "2024-12-20", False, "date_start"),
            (1, "2024-12-15", "invalid-date", False, "date_end"),
            (1, "2024/12/15", "2024-12-20", False, "date_start"),  # неправильный формат
            # Несуществующая комната
            (999, "2024-12-15", "2024-12-20", False, "room"),
            # Пустые поля
            (None, "2024-12-15", "2024-12-20", False, "room"),
            (1, None, "2024-12-20", False, "date_start"),
            (1, "2024-12-15", None, False, "date_end"),
        ],
    )
    @pytest.mark.django_db(transaction=True)
    def test_booking_field_validation(
        self,
        sample_room,
        room_id,
        date_start,
        date_end,
        should_be_valid,
        expected_error_field,
    ):
        """Тест валидации форматов полей бронирования"""
        data = {
            "room": room_id if room_id else None,
            "date_start": date_start,
            "date_end": date_end,
        }

        # Если room_id = 1, используем существующую комнату
        if room_id == 1:
            data["room"] = sample_room.id

        serializer = BookingSerializer(data=data)
        is_valid = serializer.is_valid()

        assert is_valid == should_be_valid

        if not should_be_valid and expected_error_field:
            assert expected_error_field in serializer.errors

    @pytest.mark.parametrize(
        "start_date,end_date,should_be_valid",
        [
            ("2026-12-15", "2026-12-20", True),
            ("2026-12-20", "2026-12-15", False),  # конец раньше начала
            ("2023-12-15", "2023-12-20", False),  # даты в прошлом
        ],
    )
    @pytest.mark.django_db
    def test_date_validation(self, sample_room, start_date, end_date, should_be_valid):
        data = {"room": sample_room.id, "date_start": start_date, "date_end": end_date}
        serializer = BookingSerializer(data=data)
        assert serializer.is_valid() == should_be_valid
