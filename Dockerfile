# =========================
# Stage 1: Base Image Setup
# =========================
FROM python:3.10-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# =========================
# Stage 2: Dependencies Installation
# =========================
FROM base AS dependencies

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# =========================
# Stage 3: Application Setup
# =========================
FROM dependencies AS app

# Copy the application code
COPY . .

# Make sure the entrypoint script is executable
RUN chmod +x ./entrypoint.sh

# Expose the port the app runs on
EXPOSE 8000

# =========================
# Stage 4: Final Stage
# =========================
FROM app AS final

# Define the entrypoint
ENTRYPOINT ["./entrypoint.sh"]