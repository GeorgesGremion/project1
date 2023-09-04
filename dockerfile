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

CMD ["/app/start.sh"]
