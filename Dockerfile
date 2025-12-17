FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn for production
RUN pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Create downloads directory
RUN mkdir -p downloads && chmod 755 downloads

# Expose port
EXPOSE 5000

# Run with Gunicorn
CMD ["gunicorn", "-c", "gunicorn_config.py", "backend.app:app"]

