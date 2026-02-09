#!/bin/bash

echo "===================================="
echo "Unity Circles - Quick Start"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✓ Dependencies installed"

# Run migrations
echo ""
echo "Setting up database..."
python3 manage.py migrate --run-syncdb

echo "✓ Database ready"

# Ask if user wants to create a superuser
echo ""
read -p "Do you want to create an admin user? (y/n): " create_admin

if [ "$create_admin" = "y" ] || [ "$create_admin" = "Y" ]; then
    python3 manage.py createsuperuser
fi

# Create test users
echo ""
read -p "Do you want to create test users for messaging? (y/n): " create_test

if [ "$create_test" = "y" ] || [ "$create_test" = "Y" ]; then
    python3 manage.py shell << EOF
from django.contrib.auth.models import User

# Create test users if they don't exist
if not User.objects.filter(username='alice').exists():
    user1 = User.objects.create_user('alice', 'alice@example.com', 'password123')
    user1.first_name = 'Alice'
    user1.last_name = 'Smith'
    user1.save()
    print('✓ Created user: alice (password: password123)')

if not User.objects.filter(username='bob').exists():
    user2 = User.objects.create_user('bob', 'bob@example.com', 'password123')
    user2.first_name = 'Bob'
    user2.last_name = 'Jones'
    user2.save()
    print('✓ Created user: bob (password: password123)')

print('')
print('Test users created successfully!')
print('Username: alice, Password: password123')
print('Username: bob, Password: password123')
EOF
fi

echo ""
echo "===================================="
echo "Setup Complete! 🎉"
echo "===================================="
echo ""
echo "To start the server, run:"
echo "  python3 manage.py runserver"
echo ""
echo "Then visit:"
echo "  http://127.0.0.1:8000/chat/"
echo ""
echo "Login with:"
echo "  Username: alice"
echo "  Password: password123"
echo ""
echo "Or:"
echo "  Username: bob"
echo "  Password: password123"
echo ""
echo "Admin panel:"
echo "  http://127.0.0.1:8000/admin/"
echo ""
echo "===================================="
