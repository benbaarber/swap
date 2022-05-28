#!/bin/bash
pip3 install --upgrade pip
pip3 install -r requirements.txt

source .env

python3 swap/app.py