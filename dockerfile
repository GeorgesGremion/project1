FROM ubuntu:latest

LABEL maintainer="Georges Gremion <georges@gremion.ch>"

RUN apt-get update -y && apt-get install -y \
    nginx \
    python3 \
    python3-venv \
    python3-dev \
    supervisor \
    git

WORKDIR /app
COPY . /app
RUN chmod +x /app/start.sh
COPY kiki-supervisor.conf /etc/supervisor/conf.d/
COPY kiki-nginx.conf /etc/nginx/sites-available/default

CMD ["/bin/start.sh"]
