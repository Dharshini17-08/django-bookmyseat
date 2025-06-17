#!/bin/bash
# Build script for Vercel deployment

echo "Starting build process..."

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run database migrations
python manage.py migrate

# Create movies with images (only if no movies exist)
python manage.py create_movies_with_images

echo "Build completed successfully!" 