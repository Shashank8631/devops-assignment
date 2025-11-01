FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure SQLite folder exists
RUN mkdir -p /app/instance

EXPOSE 5000

# Run Flask using Gunicorn
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:5000", "app:app"]
