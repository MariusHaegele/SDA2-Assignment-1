# Verwende ein leichtgewichtiges Python-Image
FROM python:3.9-slim

# Arbeitsverzeichnis setzen
WORKDIR /app

# Abhängigkeiten kopieren und installieren
COPY requirements.txt .
RUN pip install -r requirements.txt

# Anwendungscode kopieren
COPY app.py .

# Standardport, der freigegeben werden soll (wird vom Docker-Compose überschrieben)
EXPOSE 8080

# Anwendung starten
CMD ["python", "app.py"]