# Use Python 3.12 slim image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        gettext \
        curl \
        nginx \
        supervisor \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements_production.txt /app/
RUN pip install --no-cache-dir -r requirements_production.txt

# Copy project
COPY . /app/

# Create directories for logs and static files
RUN mkdir -p /var/log/django /app/staticfiles /app/media

# Collect static files
RUN python manage.py collectstatic --noinput --settings=womens_wear_ecommerce.settings_production

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app /var/log/django
USER app

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Start command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "womens_wear_ecommerce.wsgi:application"]
