#!/bin/bash

echo "================================================"
echo "Handwriting Recognition System - FastAPI Edition"
echo "Installation Script"
echo "================================================"
echo ""


RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' 


echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.8"

if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" = "$required_version" ]; then 
    echo -e "${GREEN}✓ Python $python_version is installed${NC}"
else
    echo -e "${RED}✗ Python 3.8 or higher is required${NC}"
    exit 1
fi


echo ""
echo "Creating virtual environment..."
if [ -d "venv" ]; then
    echo -e "${YELLOW}⚠ Virtual environment already exists${NC}"
    read -p "Do you want to recreate it? (y/N) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm -rf venv
        python3 -m venv venv
        echo -e "${GREEN}✓ Virtual environment recreated${NC}"
    fi
else
    python3 -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi


echo ""
echo "Activating virtual environment..."
source venv/bin/activate || . venv/Scripts/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"


echo ""
echo "Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo -e "${GREEN}✓ Pip upgraded${NC}"


echo ""
echo "Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements_fastapi.txt
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi


echo ""
echo "Creating necessary directories..."
mkdir -p models/model_history
mkdir -p data/uploaded/{images,documents,drawings}
mkdir -p data/custom_dataset
mkdir -p data/exports
mkdir -p static/{css,images}
mkdir -p logs
echo -e "${GREEN}✓ Directories created${NC}"


echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}⚠ Please edit .env file with your configuration${NC}"
else
    echo -e "${YELLOW}⚠ .env file already exists${NC}"
fi


echo ""
echo "Initializing database..."
python3 -c "from database import db_manager; print('Database initialized')" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Database initialized${NC}"
else
    echo -e "${YELLOW}⚠ Database initialization skipped (will be created on first run)${NC}"
fi


echo ""
if [ -f "models/handwriting_model.h5" ]; then
    echo -e "${GREEN}✓ Pre-trained model found${NC}"
else
    echo -e "${YELLOW}⚠ No pre-trained model found${NC}"
    echo "  You can train a model using:"
    echo "  1. Web interface: http://localhost:8000 (after starting server)"
    echo "  2. Command line: python model_trainer.py"
fi


echo ""
echo "================================================"
echo -e "${GREEN}Installation Complete!${NC}"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Start the server:"
echo "   python start_server.py"
echo ""
echo "2. Open your browser:"
echo "   http://localhost:8000"
echo ""
echo "3. View API documentation:"
echo "   http://localhost:8000/docs"
echo ""
echo "For more information, read:"
echo "- QUICKSTART.md for quick start guide"
echo "- README_FASTAPI.md for detailed documentation"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate  (Linux/Mac)"
echo "  .\\venv\\Scripts\\activate  (Windows)"
echo ""
echo "Happy coding! 🚀"
