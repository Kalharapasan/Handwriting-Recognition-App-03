#!/bin/bash
# Mac/Linux Startup Script for Handwriting Recognition System


RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo "================================================"
echo "Handwriting Recognition System - FastAPI"
echo "================================================"
echo ""


if ! command -v python3 &> /dev/null; then
    echo -e "${RED}[!] Python 3 is not installed${NC}"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo -e "${GREEN}[✓] Python is installed${NC}"
echo ""


if [ -d "venv" ]; then
    echo -e "${BLUE}[*] Activating virtual environment...${NC}"
    source venv/bin/activate
else
    echo -e "${YELLOW}[!] No virtual environment found${NC}"
    echo -e "${BLUE}[*] Creating virtual environment...${NC}"
    python3 -m venv venv
    source venv/bin/activate
    
    echo -e "${BLUE}[*] Installing dependencies...${NC}"
    pip install --upgrade pip
    pip install -r requirements_fastapi.txt
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}[!] Failed to install dependencies${NC}"
        exit 1
    fi
fi

echo ""
echo -e "${BLUE}[*] Creating necessary directories...${NC}"
mkdir -p models/model_history
mkdir -p data/uploaded/images
mkdir -p data/uploaded/documents
mkdir -p data/uploaded/drawings
mkdir -p data/custom_dataset
mkdir -p data/exports
mkdir -p static/css
mkdir -p static/images
mkdir -p logs

echo ""
echo -e "${GREEN}[*] Starting server...${NC}"
echo -e "${BLUE}[*] The server will start on http://localhost:8000${NC}"
echo -e "${YELLOW}[*] Press Ctrl+C to stop the server${NC}"
echo ""
echo "================================================"
echo ""


python server.py

if [ $? -ne 0 ]; then
    echo ""
    echo -e "${RED}[!] Server stopped with error${NC}"
    exit 1
fi
