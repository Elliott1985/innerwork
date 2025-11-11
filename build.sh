#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations (create tables)
python -c "from app import create_app; from models import db; app = create_app(); app.app_context().push(); db.create_all(); print('Database tables created successfully')"
