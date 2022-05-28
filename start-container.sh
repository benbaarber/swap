#!/bin/bash

echo ">>> Starting app."
alembic upgrade head
python3 /opt/swap/swap/app.py