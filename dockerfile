FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y python3 python3-venv python3-dev mysql-server postfix mailutils supervisor nginx git openssl

COPY . /app
WORKDIR /app

ENV FLASK_APP=kiki.py

RUN python3 -m venv venv
RUN . venv/bin/activate && pip install -r requirements.txt && pip install gunicorn pymysql cryptography

# Hier können Sie weitere Konfigurationsschritte für Postfix, MySQL usw. hinzufügen ...

# Exponieren Sie den gewünschten Port (z. B. 80 für HTTP und 443 für HTTPS)
EXPOSE 80 443

# Starten Sie Ihre Anwendung (dies kann durch ein Startskript oder direkt hier erfolgen)
CMD ["nginx", "-g", "daemon off;"]
