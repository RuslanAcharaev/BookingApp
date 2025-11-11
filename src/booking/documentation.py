from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    extend_schema,
    extend_schema_view,
)

from .serializers import BookingSerializer, RoomSerializer

room_schema = extend_schema_view(
    list=extend_schema(
        summary="Получить список всех номеров",
        description="Возвращает список всех номеров c возможностью сортировки по цене и ID.",
        parameters=[
            OpenApiParameter(
                name="ordering",
                description='Сортировка по полям: id, price, description. Для убывания используйте префикс "-"',
                required=False,
                type=str,
                examples=[
                    OpenApiExample("По возрастанию цены", value="price"),
                    OpenApiExample("По убыванию цены", value="-price"),
                    OpenApiExample("По возрастанию ID", value="id"),
                ],
            )
        ],
        responses={200: RoomSerializer(many=True)},
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                value=[
                    {
                        "id": 1,
                        "description": "Стандартный номер c видом на город",
                        "price": 5000.00,
                    },
                    {
                        "id": 2,
                        "description": "Люкс c видом на море",
                        "price": 15000.00,
                    },
                ],
                response_only=True,
                status_codes=["200"],
            )
        ],
    ),
    retrieve=extend_schema(
        summary="Получить информацию o номере по ID",
        description="Возвращает полную информацию o конкретном номере.",
        responses={200: RoomSerializer},
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="Уникальное целое число, идентифицирующее номер.",
                required=True,
                type=int,
            )
        ],
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "id": 1,
                    "description": "Стандартный номер c видом на город",
                    "price": 5000.00,
                },
                response_only=True,
                status_codes=["200"],
            )
        ],
    ),
    create=extend_schema(
        summary="Создать новый номер",
        description="Создает новый номер в системе.",
        responses={201: RoomSerializer},
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={"description": "Новый улучшенный номер", "price": "7500.00"},
                request_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "id": 3,
                    "description": "Новый улучшенный номер",
                    "price": 7500.00,
                },
                response_only=True,
                status_codes=["201"],
            ),
        ],
    ),
    update=extend_schema(
        summary="Полное обновление номера",
        description="Полностью обновляет информацию o номере. Bce поля обязательны.",
        responses={200: RoomSerializer},
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="ID обновляемого номера",
                required=True,
                type=int,
            )
        ],
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={
                    "description": "Обновленное описание номера",
                    "price": 8500.00,
                },
                request_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "id": 1,
                    "description": "Обновленное описание номера",
                    "price": 8500.00,
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление номера",
        description="Частично обновляет информацию o номере. Можно передать только изменяемые поля.",
        responses={200: RoomSerializer},
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="ID обновляемого номера",
                required=True,
                type=int,
            )
        ],
        examples=[
            OpenApiExample(
                "Пример запроса (только цена)",
                value={"price": 9000.00},
                request_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример запроса (только описание)",
                value={"description": "Новое описание номера"},
                request_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "id": 1,
                    "description": "Новое описание номера",
                    "price": 9000.00,
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
    destroy=extend_schema(
        summary="Удалить номер",
        description="Удаляет номер из системы.",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="ID удаляемого номера",
                required=True,
                type=int,
            )
        ],
        responses={204: None},
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                description="При успешном удалении возвращается статус 204 без содержимого",
                value=None,
                response_only=True,
                status_codes=["204"],
            )
        ],
    ),
)

booking_schema = extend_schema_view(
    list=extend_schema(
        summary="Получить список бронирований для конкретной комнаты",
        description="Возвращает список бронирований для указанной комнаты, отсортированных по дате начала.",
        parameters=[
            OpenApiParameter(
                name="room_id",
                description="ID комнаты для фильтрации бронирований",
                required=True,
                type=int,
                examples=[
                    OpenApiExample("Пример room_id", value=1),
                ],
            )
        ],
        responses={200: BookingSerializer(many=True), 400: BookingSerializer},
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                value=[
                    {
                        "id": 1,
                        "room": 1,
                        "date_start": "2024-12-15",
                        "date_end": "2024-12-20",
                    },
                    {
                        "id": 2,
                        "room": 1,
                        "date_start": "2024-12-25",
                        "date_end": "2024-12-28",
                    },
                ],
                response_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример ошибки - не указан room_id",
                value={"error": "Необходимо указать room_id"},
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
    retrieve=extend_schema(
        summary="Получить информацию o бронировании по ID",
        description="Возвращает полную информацию o конкретном бронировании.",
        responses={200: BookingSerializer},
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="Уникальное целое число, идентифицирующее бронирование.",
                required=True,
                type=int,
            )
        ],
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "id": 1,
                    "room": 1,
                    "date_start": "2024-12-15",
                    "date_end": "2024-12-20",
                },
                response_only=True,
                status_codes=["200"],
            )
        ],
    ),
    create=extend_schema(
        summary="Создать новое бронирование",
        description="Создает новое бронирование c проверкой доступности комнаты на указанные даты.",
        responses={201: BookingSerializer, 400: BookingSerializer},
        examples=[
            OpenApiExample(
                "Пример успешного запроса",
                value={"room": 1, "date_start": "2024-12-15", "date_end": "2024-12-20"},
                request_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "id": 3,
                    "room": 1,
                    "date_start": "2024-12-15",
                    "date_end": "2024-12-20",
                },
                response_only=True,
                status_codes=["201"],
            ),
            OpenApiExample(
                "Пример ошибки - комната занята",
                value={"room": ["Комната уже забронирована на указанные даты"]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Пример ошибки - некорректные даты",
                value={"date_end": ["Дата окончания не может быть раньше даты начала"]},
                response_only=True,
                status_codes=["400"],
            ),
            OpenApiExample(
                "Пример ошибки - дата в прошлом",
                value={"date_start": ["Нельзя бронировать на прошедшие даты"]},
                response_only=True,
                status_codes=["400"],
            ),
        ],
    ),
    update=extend_schema(
        summary="Полное обновление бронирования",
        description="Полностью обновляет информацию o бронировании. Bce поля обязательны.",
        responses={200: BookingSerializer},
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="ID обновляемого бронирования",
                required=True,
                type=int,
            )
        ],
        examples=[
            OpenApiExample(
                "Пример запроса",
                value={"room": 1, "date_start": "2024-12-16", "date_end": "2024-12-21"},
                request_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "id": 1,
                    "room": 1,
                    "date_start": "2024-12-16",
                    "date_end": "2024-12-21",
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
    partial_update=extend_schema(
        summary="Частичное обновление бронирования",
        description="Частично обновляет информацию o бронировании. Можно передать только изменяемые поля.",
        responses={200: BookingSerializer},
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="ID обновляемого бронирования",
                required=True,
                type=int,
            )
        ],
        examples=[
            OpenApiExample(
                "Пример запроса (только даты)",
                value={"date_start": "2024-12-17", "date_end": "2024-12-22"},
                request_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример запроса (только комната)",
                value={"room": 2},
                request_only=True,
                status_codes=["200"],
            ),
            OpenApiExample(
                "Пример успешного ответа",
                value={
                    "id": 1,
                    "room": 2,
                    "date_start": "2024-12-17",
                    "date_end": "2024-12-22",
                },
                response_only=True,
                status_codes=["200"],
            ),
        ],
    ),
    destroy=extend_schema(
        summary="Удалить бронирование",
        description="Удаляет бронирование из системы.",
        parameters=[
            OpenApiParameter(
                name="id",
                location=OpenApiParameter.PATH,
                description="ID удаляемого бронирования",
                required=True,
                type=int,
            )
        ],
        responses={204: None},
        examples=[
            OpenApiExample(
                "Пример успешного ответа",
                description="При успешном удалении возвращается статус 204 без содержимого",
                value=None,
                response_only=True,
                status_codes=["204"],
            )
        ],
    ),
)
