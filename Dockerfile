FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN apt-get update && apt-get install -y --no-install-recommends gcc && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install \
    --no-cache-dir \
    --default-timeout=100 \
    --retries=10 \
    -r requirements.txt
COPY . .
CMD ["bash", "scripts/bootstrap.sh"]
