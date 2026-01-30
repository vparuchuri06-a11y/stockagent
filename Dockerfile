# Use Python 3.11 (stable + Cloud Run friendly)
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Cloud Run listens on this port
EXPOSE 7860

# Start the app
CMD ["python", "outsideapp.py"]
