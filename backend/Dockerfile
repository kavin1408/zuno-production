# Use standard Python image (not slim) for maximum compatibility
FROM python:3.11

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies (even if not strictly needed for standard wheels, safety first)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
# --no-cache-dir to keep image small-ish, but upgrade pip first
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose the port (Railway sends PORT env var, but we document it)
# Expose is handled by Railway internally

# Command to run the application using Uvicorn
# We explicitly bind to 0.0.0.0 and use the PORT env var
CMD ["python", "main.py"]
