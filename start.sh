#!/bin/bash

/app/venv/bin/flask db init
/app/venv/bin/flask db migrate
/app/venv/bin/flask db upgrade

nginx -g "daemon off;"

supervisorctl reload
supervisorctl start kiki