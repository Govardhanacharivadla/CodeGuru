#!/bin/bash
# Daily commit helper for CodeGuru

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 CodeGuru Daily Commit${NC}\n"

# Check if there are changes
if [[ -z $(git status -s) ]]; then
    echo -e "${YELLOW}No changes to commit!${NC}"
    exit 0
fi

# Show status
echo -e "${GREEN}📊 Changes:${NC}"
git status -s
echo ""

# Ask for commit message
echo -e "${BLUE}What did you work on today?${NC}"
read -p "Commit message: " message

# If no message, use default
if [ -z "$message" ]; then
    message="Daily update: $(date +%Y-%m-%d)"
fi

# Add all changes
git add .

# Commit
git commit -m "🔄 $message"

# Push
echo -e "\n${GREEN}📤 Pushing to GitHub...${NC}"
git push

echo -e "\n${GREEN}✅ Daily commit complete!${NC}"
echo -e "${BLUE}Keep building! 💪${NC}\n"
