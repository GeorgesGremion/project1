# VCID.IA1A.PA Praxisarbeit - Arbeit der IPSO Bildung

Die Kita APP von Georges Gremion

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

Die Container sind öffentlich unter Docker Hub zu finden:

        https://hub.docker.com/repository/docker/gjoker86/project1_app
        https://hub.docker.com/repository/docker/gjoker86/project1_mysql/general

Beispieldaten Importieren (beide Varianten):

        ./install_sampledata.sh

Nun sind einige Kinder angelegt, sowie der Benutzer admin mit dem Passwort admin

Viel Spass!
