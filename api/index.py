"""
Vercel serverless handler for Flask application.
This file acts as the entry point for Vercel's serverless functions.
"""
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app

# Create Flask app instance
app = create_app()

# Vercel serverless function handler
def handler(request, context):
    return app(request, context)

# For local development
if __name__ == "__main__":
    app.run()
