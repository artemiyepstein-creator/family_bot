FROM python:3.12-slim

WORKDIR /app

# системные зависимости (psycopg/asyncpg обычно хватает без них, но на всякий — можно оставить минимально)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# код
COPY . /app

# запуск
CMD ["python", "-m", "app.main"]