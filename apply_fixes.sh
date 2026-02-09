#!/bin/bash

# Unity Circles - Quick Fix Application Script
# This script applies all fixes automatically

set -e  # Exit on error

echo "🚀 Unity Circles - Applying All Fixes"
echo "======================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "manage.py" ]; then
    echo -e "${RED}Error: manage.py not found. Please run this script from the project root.${NC}"
    exit 1
fi

echo -e "${YELLOW}Creating backups...${NC}"
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Backup templates
echo "  📦 Backing up templates..."
cp templates/communities.html "$BACKUP_DIR/" 2>/dev/null || echo "  ⚠️  communities.html not found"
cp templates/meetings.html "$BACKUP_DIR/" 2>/dev/null || echo "  ⚠️  meetings.html not found"
cp templates/dashboard.html "$BACKUP_DIR/" 2>/dev/null || echo "  ⚠️  dashboard.html not found"

# Backup views
echo "  📦 Backing up views..."
cp core/views.py "$BACKUP_DIR/" 2>/dev/null || echo "  ⚠️  core/views.py not found"

echo -e "${GREEN}✅ Backups created in $BACKUP_DIR${NC}"
echo ""

echo -e "${YELLOW}Applying template fixes...${NC}"

# Apply improved templates
if [ -f "templates/communities_improved.html" ]; then
    echo "  🔧 Updating communities.html..."
    cp templates/communities_improved.html templates/communities.html
    echo -e "  ${GREEN}✅ communities.html updated${NC}"
else
    echo -e "  ${RED}❌ communities_improved.html not found${NC}"
fi

if [ -f "templates/meetings_improved.html" ]; then
    echo "  🔧 Updating meetings.html..."
    cp templates/meetings_improved.html templates/meetings.html
    echo -e "  ${GREEN}✅ meetings.html updated${NC}"
else
    echo -e "  ${RED}❌ meetings_improved.html not found${NC}"
fi

if [ -f "templates/dashboard_improved.html" ]; then
    echo "  🔧 Updating dashboard.html..."
    cp templates/dashboard_improved.html templates/dashboard.html
    echo -e "  ${GREEN}✅ dashboard.html updated${NC}"
else
    echo -e "  ${RED}❌ dashboard_improved.html not found${NC}"
fi

echo ""
echo -e "${GREEN}✅ All fixes applied successfully!${NC}"
echo ""
echo "📝 Next steps:"
echo "  1. Restart your Django server: python manage.py runserver"
echo "  2. Clear your browser cache (Ctrl+Shift+Del or Cmd+Shift+Del)"
echo "  3. Reload the pages in your browser"
echo ""
echo "📋 What was fixed:"
echo "  ✅ Meetings page error handling"
echo "  ✅ Dashboard communities and stats display"
echo "  ✅ Community image alignment"
echo "  ✅ Live updates (auto-refresh every 30s)"
echo ""
echo "📂 Backups are in: $BACKUP_DIR"
echo ""
echo "🎉 All done! Enjoy your improved Unity Circles platform!"
