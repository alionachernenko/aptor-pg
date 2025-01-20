FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=8000 \
    HOST=0.0.0.0

EXPOSE ${PORT}

CMD ["uvicorn", "main:app", "--host", ${HOST}, "--port", ${PORT}]