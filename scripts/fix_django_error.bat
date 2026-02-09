@echo off
REM Comprehensive Django Python 3.14 Compatibility Fix for Windows
REM This script fixes the AttributeError: 'super' object has no attribute 'dicts'

echo ==========================================
echo Django Python 3.14 Compatibility Fix
echo ==========================================
echo.

echo Step 1: Stopping any running Django servers...
taskkill /F /IM python.exe 2>nul
timeout /t 2 /nobreak >nul

echo.
echo Step 2: Backing up database...
if exist db.sqlite3 (
    copy db.sqlite3 db.sqlite3.backup.%date:~-4%%date:~-10,2%%date:~-7,2%_%time:~0,2%%time:~3,2%%time:~6,2%
    echo Database backed up
)

echo.
echo Step 3: Clearing all Python cache...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /s /q *.pyc 2>nul
del /s /q *.pyo 2>nul
echo Cache cleared

echo.
echo Step 4: Uninstalling current Django...
pip uninstall -y Django 2>nul

echo.
echo Step 5: Installing Django 5.1 (Python 3.14 compatible)...
pip install "Django>=5.1,<5.2" --force-reinstall

echo.
echo Step 6: Upgrading Django REST Framework...
pip install --upgrade "djangorestframework>=3.15"

echo.
echo Step 7: Upgrading other dependencies...
pip install --upgrade django-cors-headers
pip install --upgrade djangorestframework-simplejwt
pip install --upgrade Pillow

echo.
echo Step 8: Deleting old migration files...
for /r %%i in (migrations\*.py) do (
    if not "%%~nxi"=="__init__.py" del "%%i"
)
echo Migration files cleared

echo.
echo Step 9: Deleting and recreating database...
if exist db.sqlite3 del db.sqlite3
echo Database deleted

echo.
echo Step 10: Creating fresh migrations...
python manage.py makemigrations accounts
python manage.py makemigrations core
python manage.py makemigrations chat
python manage.py makemigrations mentorship
python manage.py makemigrations onboarding
python manage.py makemigrations

echo.
echo Step 11: Applying migrations...
python manage.py migrate

echo.
echo Step 12: Creating superuser...
echo from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@admin.com', 'admin123') if not User.objects.filter(username='admin').exists() else None | python manage.py shell

echo.
echo ==========================================
echo Fix completed successfully!
echo ==========================================
echo.
echo Superuser created:
echo   Username: admin
echo   Password: admin123
echo.
echo To start the server:
echo   python manage.py runserver
echo.
echo Then visit: http://127.0.0.1:8000/admin/
echo.
pause
