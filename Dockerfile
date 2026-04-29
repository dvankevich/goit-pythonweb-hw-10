# Стейдж 1: Збірка залежностей
FROM python:3.13-slim AS builder

# Встановлюємо системні залежності для збірки (наприклад, для psycopg2)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Налаштовуємо Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

# Встановлюємо poetry
RUN pip install poetry==2.0.1

# Копіюємо файли конфігурації залежностей
COPY pyproject.toml poetry.lock ./

# Встановлюємо тільки основні залежності застосунку
RUN poetry install --only main --no-root && rm -rf $POETRY_CACHE_DIR

# Стейдж 2: Фінальний образ
FROM python:3.13-slim AS runtime

# Встановлюємо libpq для роботи з PostgreSQL
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Копіюємо встановлені залежності з першого стейджу
COPY --from=builder /app/.venv /app/.venv

# Копіюємо код застосунку
COPY . .

# Експонуємо порт
EXPOSE 8000

# Запускаємо застосунок через uvicorn
# Зверніть увагу: main:app має відповідати вашій точці входу
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]