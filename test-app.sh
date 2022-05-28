#!/bin/bash
pip3 install --upgrade pip
pip3 install -r requirements.txt

source .env

createdb test-db

# Enter your local db url
export DATABASE_URL="postgres://benbarber@localhost:5432/test-db"

alembic upgrade head

pytest

dropdb test-db

source .env

echo ">>> Local Testing Complete"

python3 tests/integration/test_auth_app.py

echo ">>> Authorization Testing Complete"