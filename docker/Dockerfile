FROM python:3.12-slim

WORKDIR /app

# системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
 && rm -rf /var/lib/apt/lists/*

# зависимости
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# код
COPY . /app

# ВАЖНО: запускаем из src, где лежит пакет app
WORKDIR /app/src
CMD ["python", "-m", "app.main"]