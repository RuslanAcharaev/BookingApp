# Booking App

Система бронирования номеров с REST API на Django и Django REST Framework.

## Установка и запуск

### Предварительные требования

- Docker и Docker Compose
- Python 3.12+ (рекомендуется использовать [uv](https://github.com/astral-sh/uv))

### Настройка окружения

1. Клонируйте репозиторий:
```bash
git clone https://github.com/RuslanAcharaev/BookingApp.git
```

2. Создайте файл `.env` на основе `.env.example`, указав необходимые настройки:
```env
DB_NAME=booking_db
DB_USER=booking_user
DB_PASSWORD=booking_password
DB_HOST=db
DB_PORT=5432
DEBUG=True
SECRET_KEY=your-secret-key-here
```

### Запуск приложения

1. Соберите и запустите контейнеры:
```bash
docker-compose up --build
```

2. Приложение будет доступно по адресу: http://localhost:8000

3. Для создания суперпользователя, если требуется, выполните в другом терминале:
```bash
docker-compose exec web python src/manage.py createsuperuser
```


## Документация API

После запуска приложения доступна интерактивная документация:

- **Swagger UI**: http://localhost:8000/api/schema/swagger-ui/
- **OpenAPI схема**: http://localhost:8000/api/schema/

Документация включает полное описание всех доступных эндпоинтов, параметров запросов, форматов данных и примеров использования.

## Тестирование

Для запуска тестов используйте команду:

```bash
docker-compose exec web pytest -v --cov=booking
```

Доступные опции тестирования:

- Запуск всех тестов: `pytest`
- Запуск с детальным выводом: `pytest -v`
- Запуск с измерением покрытия: `pytest --cov=booking`
- Запуск конкретного тестового файла: `pytest src/booking/tests/test_models.py`

Тесты написаны с использованием pytest и покрывают модели, сериализаторы и API эндпоинты.

## Структура проекта

```
src/
├── core/                   # Настройки проекта
├── booking/                # Приложение бронирования
│   ├── tests/              # Тесты
│   ├── models.py           # Модели данных
│   ├── serializers.py      # Сериализаторы
│   ├── views.py            # Вьюсеты
│   ├── urls.py             # Роутинг
│   └── documentation.py    # Документация
└── manage.py
```
