#!/bin/bash

# Color codes for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up Python virtual environment...${NC}"

# Create virtual environment
python3 -m venv venv

echo -e "${GREEN}Virtual environment created${NC}"

# Activate virtual environment
source venv/bin/activate

echo -e "${YELLOW}Installing dependencies...${NC}"

# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

echo -e "${GREEN}Dependencies installed successfully!${NC}"
echo ""
echo -e "${YELLOW}To activate the virtual environment in future sessions, run:${NC}"
echo "source venv/bin/activate"
echo ""
echo -e "${YELLOW}To run the application:${NC}"
echo "python main.py"
echo ""
echo -e "${YELLOW}To deactivate the virtual environment:${NC}"
echo "deactivate"
