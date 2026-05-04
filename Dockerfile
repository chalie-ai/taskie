FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libmariadb-dev-compat supervisor && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn==23.0.0

COPY . .

RUN mkdir -p instance

EXPOSE 8080 5100

CMD ["supervisord", "-c", "/app/supervisord.conf"]
