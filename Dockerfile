# 1. Base image (must be first line)
FROM python:3.11-slim

# 2. Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# 3. Install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    tesseract-ocr \
    libtesseract-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# 4. Working directory inside the container
WORKDIR /app

# 5. Copy requirements file
COPY requirements.txt /app/requirements.txt

# 6. Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# 7. Copy the rest of your project
COPY . /app

# 8. Environment for tesseract binary path
ENV TESSERACT_CMD=/usr/bin/tesseract

# 9. Expose port (documentation only, doesn’t actually publish)
EXPOSE 5000

# 10. Entrypoint / command to run
ENTRYPOINT ["sh","-c","gunicorn -w 4 -b 0.0.0.0:${PORT:-5000} app:app"]
