FROM python:3.8-alpine AS builder
LABEL authors="thedjaney@gmail.com"

WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.8-alpine
WORKDIR /app
COPY . .
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
CMD ["python", "worker.py"]