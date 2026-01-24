FROM python:3.10-slim

WORKDIR /app

# Install system dependencies if needed (e.g. for psycopg2)
# libpq-dev is often needed for psycopg2, but psycopg2-binary usually avoids this
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Expose the port (Railway ignores EXPOSE but it's good practice)
EXPOSE 8000

# Start command
CMD ["python", "main.py"]
