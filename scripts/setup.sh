#!/bin/bash

echo "======================================================"
echo "Unity Circles - Setup Script"
echo "======================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt --break-system-packages 2>/dev/null || pip install -r requirements.txt
echo ""

# Run migrations
echo "🔄 Running database migrations..."
python3 manage.py migrate
echo ""

# Create media directories
echo "📁 Creating media directories..."
mkdir -p media/community_images
mkdir -p media/post_images
chmod -R 755 media
echo ""

# Check if superuser exists
echo "👤 Checking for superuser..."
python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); print('Superuser exists' if User.objects.filter(is_superuser=True).exists() else 'No superuser')" | grep -q "No superuser"

if [ $? -eq 0 ]; then
    echo "❓ Would you like to create a superuser? (y/n)"
    read -r response
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        python3 manage.py createsuperuser
    fi
fi
echo ""

echo "======================================================"
echo "✅ Setup Complete!"
echo "======================================================"
echo ""
echo "To start the development server:"
echo "  python3 manage.py runserver"
echo ""
echo "Then open your browser to:"
echo "  http://127.0.0.1:8000/"
echo ""
echo "Admin panel:"
echo "  http://127.0.0.1:8000/admin/"
echo ""
echo "======================================================"
