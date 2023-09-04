# Verwenden Sie ein offizielles Python-Laufzeit-Image als Eltern-Image
FROM python:3.8-slim-buster

# Setzen Sie das Arbeitsverzeichnis im Container
WORKDIR /app

# Kopieren Sie die aktuellen Verzeichnisinhalte in den Container unter /app
COPY . /app

# Installieren Sie alle benötigten Pakete
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Legen Sie die Umgebungsvariable fest, um sicherzustellen, dass Python keine .pyc-Dateien im Container erstellt
ENV PYTHONDONTWRITEBYTECODE 1

# Legen Sie die Umgebungsvariable fest, um sicherzustellen, dass Flask im Debug-Modus ausgeführt wird
ENV FLASK_APP kiki.py
ENV FLASK_RUN_HOST 0.0.0.0

# Öffnen Sie den Port 5000
EXPOSE 5000

# Definieren Sie den Befehl zum Ausführen der Container-Anwendung
CMD ["flask", "run"]
