FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# system deps
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# project
COPY . .

CMD ["python", "bot/main.py"]
