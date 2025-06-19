FROM python:alpine

WORKDIR /app

RUN adduser -D -s /bin/sh appuser

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p /app/logs

RUN chown -R appuser:appuser /app/logs

RUN chmod -R 755 /app/logs

RUN chown -R appuser:appuser /app

USER appuser