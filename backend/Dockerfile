FROM python:3.9-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка зависимостей для GDAL
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка GDAL
ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal
RUN pip install GDAL==$(gdal-config --version) --no-cache-dir

COPY . .

CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:8000"]