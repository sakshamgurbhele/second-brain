#!/bin/bash
set -e

echo "=== Setting up second-brain ==="

# Install Python 3.12 if not present
if ! python3.12 --version &>/dev/null; then
  sudo apt update -y
  sudo apt install -y python3.12 python3.12-venv python3.12-dev
fi

# Clone repo
cd /home/ubuntu
if [ -d ".git" ]; then
  git pull
else
  git clone https://github.com/sakshamgurbhele/second-brain.git temp_clone
  cp -r temp_clone/. .
  rm -rf temp_clone
fi

# Create virtualenv
python3.12 -m venv todoenv

# Install dependencies
todoenv/bin/pip install --upgrade pip -q
todoenv/bin/pip install -r todoproject/requirements.txt -q

# Create .env if missing
if [ ! -f .env ]; then
  SECRET=$(python3.12 -c "import secrets; print(secrets.token_urlsafe(50))")
  cat > .env <<EOF
DJANGO_SECRET_KEY=$SECRET
DJANGO_DEBUG=false
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost,$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
BASE_PASSWORD=changeme
EOF
  echo ">>> .env created — update BASE_PASSWORD and ALLOWED_HOSTS as needed"
fi

# Run migrations
set -a && source .env && set +a
cd todoproject
../todoenv/bin/python manage.py migrate --run-syncdb

echo "=== Setup complete. Run: bash start_server.sh ==="
