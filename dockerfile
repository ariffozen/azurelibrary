# Base image olarak Python 3.9 kullan
FROM python:3.9

# Çalışma dizinini oluştur
WORKDIR /app

# Bağımlılıkları kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Flask uygulamasını kopyala
COPY . .

# Flask uygulamasını başlat
CMD ["python", "app.py"]

