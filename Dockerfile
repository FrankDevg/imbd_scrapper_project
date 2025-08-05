FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Instala dependencias del sistema, incluyendo postgresql-client
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    tor \
    curl \
    netcat-openbsd \
    gnupg \
    ca-certificates \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia e instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del proyecto
COPY . .

# Comando por defecto
CMD ["python", "presentation/cli/run_scraper.py"]
