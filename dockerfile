# Verwenden Sie das offizielle Ubuntu-Image als Basis
FROM ubuntu:latest

# Setze den Maintainer des Images
LABEL maintainer="Ihr Name <ihre-email@example.com>"

# Aktualisieren Sie die Paketlisten und installieren Sie die erforderlichen Pakete
RUN apt-get update -y && apt-get install -y \
    nginx \
    python3 \
    python3-venv \
    python3-dev \
    supervisor \
    git

# Erstellen Sie das Verzeichnis für Ihre Anwendung
WORKDIR /app
COPY . /app

COPY kiki-supervisor.conf /etc/supervisor/conf.d/
COPY kiki-nginx.conf /etc/nginx/sites-available/default

RUN python3 -m venv venv

RUN /app/venv/bin/pip3 install -r requirements.txt

ENV FLASK_APP /app/kiki.py

RUN /app/venv/bin/flask db init

RUN /app/venv/bin/flask db migrate

RUN /app/venv/bin/flask db upgrade


# Hier können Sie weitere Befehle hinzufügen, um Ihre Anwendung zu konfigurieren, 
# z.B. das Kopieren von Konfigurationsdateien für Nginx oder Supervisor.

# Startbefehl, wenn der Container läuft (ändern Sie dies entsprechend Ihrer Anforderungen)
CMD ["nginx", "-g", "daemon off;"]
