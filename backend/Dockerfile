FROM python:3.13-slim

ENV PYTHONPATH=/app

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY req.txt .

RUN pip install --upgrade pip && pip install --no-cache-dir -r req.txt

COPY . .

EXPOSE 8000

HEALTHCHECK CMD ["curl", "--fail", "http://localhost:8000", "||", "exit 1"]

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]