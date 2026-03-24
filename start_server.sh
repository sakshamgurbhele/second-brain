#!/bin/bash
set -a
source /home/ubuntu/.env
set +a
source /home/ubuntu/todoenv/bin/activate
cd /home/ubuntu/todoproject
exec gunicorn --workers 3 --bind 127.0.0.1:8000 --timeout 60 todoproject.wsgi:application
