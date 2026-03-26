#!/bin/bash
DIR="$(cd "$(dirname "$0")" && pwd)"

set -a
source "$DIR/.env"
set +a

source "$DIR/todoenv/bin/activate"
cd "$DIR"
exec gunicorn --workers 3 --bind 127.0.0.1:8000 --timeout 60 todoproject.wsgi:application
