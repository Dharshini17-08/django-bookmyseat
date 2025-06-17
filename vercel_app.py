import os
import sys
from pathlib import Path

# Add the project directory to the Python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookmyseat.settings')

# Import Django and set up the application
import django
django.setup()

# Import the WSGI application
from bookmyseat.wsgi import application

# Export the application for Vercel
app = application

# For Vercel serverless functions
def handler(request, context):
    return app(request, context) 