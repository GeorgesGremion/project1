# project1

Im Rahmen einer IPSO Ausbildung...

Die Kita APP

# Installation

Download des repositorys:
        git clone https://github.com/GeorgesGremion/project1.git

Vorbereiten der Dateien:
        cd project1
        chmod +x start.sh
        chmod +x install_sampledata.sh

Nun kann die App manuell aus dem Dockerfile erstellt werden, oder die Container via Docker Hub (EMPFOHLEN) installiert werden.

Manuelles erstellen der Container:
        docker compose build
        docker compose up -d
        docker exec -it project1-app-1 bash
        ./start.sh

Nun sind ist ein Container für die Kita APP, für die DB (MySQL) und ein PHPMyAdmin erstellt.

Erstellen via Docker Hub (EMPFOHLEN):
        docker compose -f compose_dockerhub.yaml up -d

Beispieldaten Importieren (beide Varianten):
        ./install_sampledata.sh

Nun sind einige Kinder angelegt, sowie der Benutzer admin mit dem Passwort admin

Viel Spass!
