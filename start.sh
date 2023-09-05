#!/bin/bash

if [ ! -f /app/.initialized ]; then
    python3 -m venv venv
    /app/venv/bin/pip3 install -r requirements.txt
    export FLASK_APP=/app/kiki.py
    /app/venv/bin/flask db init
    /app/venv/bin/flask db migrate
    /app/venv/bin/flask db upgrade
    touch /app/.initialized
fi

export FLASK_APP=/app/kiki.py
service supervisor start
supervisorctl reload
supervisorctl start kiki
nginx -g "daemon off;"
