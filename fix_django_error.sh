#!/bin/bash

# Comprehensive Django Python 3.14 Compatibility Fix
# This script fixes the AttributeError: 'super' object has no attribute 'dicts'

echo "=========================================="
echo "Django Python 3.14 Compatibility Fix"
echo "=========================================="
echo ""

# Get the current directory
PROJECT_DIR=$(pwd)

echo "Step 1: Stopping any running Django servers..."
pkill -f "python.*manage.py runserver" 2>/dev/null || true
sleep 2

echo ""
echo "Step 2: Backing up database..."
if [ -f "db.sqlite3" ]; then
    cp db.sqlite3 db.sqlite3.backup.$(date +%Y%m%d_%H%M%S)
    echo "✓ Database backed up"
fi

echo ""
echo "Step 3: Clearing all Python cache..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
echo "✓ Cache cleared"

echo ""
echo "Step 4: Uninstalling current Django..."
pip uninstall -y Django 2>/dev/null || true

echo ""
echo "Step 5: Installing Django 5.1 (Python 3.14 compatible)..."
pip install "Django>=5.1,<5.2" --break-system-packages --force-reinstall

echo ""
echo "Step 6: Upgrading Django REST Framework..."
pip install --upgrade "djangorestframework>=3.15" --break-system-packages

echo ""
echo "Step 7: Upgrading other dependencies..."
pip install --upgrade django-cors-headers --break-system-packages
pip install --upgrade djangorestframework-simplejwt --break-system-packages
pip install --upgrade Pillow --break-system-packages

echo ""
echo "Step 8: Deleting migration files (will be recreated)..."
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete 2>/dev/null || true
find . -path "*/migrations/*.pyc" -delete 2>/dev/null || true
echo "✓ Migration files cleared"

echo ""
echo "Step 9: Deleting and recreating database..."
rm -f db.sqlite3
echo "✓ Database deleted"

echo ""
echo "Step 10: Creating fresh migrations..."
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py makemigrations chat
python manage.py makemigrations mentorship
python manage.py makemigrations onboarding
python manage.py makemigrations

echo ""
echo "Step 11: Applying migrations..."
python manage.py migrate

echo ""
echo "Step 12: Creating superuser..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin123') if not User.objects.filter(username='admin').exists() else None" | python manage.py shell

echo ""
echo "=========================================="
echo "✓ Fix completed successfully!"
echo "=========================================="
echo ""
echo "Superuser created:"
echo "  Username: admin"
echo "  Password: admin123"
echo ""
echo "To start the server:"
echo "  python manage.py runserver"
echo ""
echo "Then visit: http://127.0.0.1:8000/admin/"
echo ""
