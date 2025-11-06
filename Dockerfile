FROM python:3.12-slim

# Устанавливаем зависимости для компиляции
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем uv
RUN pip install uv

WORKDIR /app

# Копируем зависимости
COPY pyproject.toml .

# Устанавливаем зависимости
RUN uv pip install --system -r pyproject.toml

# Копируем исходный код
COPY . .

EXPOSE 8000
