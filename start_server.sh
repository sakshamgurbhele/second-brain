#!/bin/bash
set -a
source /home/ubuntu/.env
set +a
source /home/ubuntu/todoenv/bin/activate
cd /home/ubuntu/todoproject
exec python manage.py runserver 0.0.0.0:8000
