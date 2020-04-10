#!/bin/sh
flask db upgrade
exec gunicorn -b :5600 --access-logfile - --error-logfile - planning-svc:app