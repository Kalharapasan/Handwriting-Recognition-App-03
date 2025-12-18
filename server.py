#!/usr/bin/env python3
import sys
import os
import subprocess
import logging
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_dependencies():
    logger.info("Checking dependencies...")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'tensorflow',
        'numpy',
        'opencv-python',
        'PIL',
        'sqlalchemy'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').split('[')[0])
        except ImportError:
            missing.append(package)
    
    if missing:
        logger.error(f"Missing required packages: {', '.join(missing)}")
        logger.info("Install them with: pip install -r requirements_fastapi.txt")
        return False
    
    logger.info("All dependencies are installed")
    return True

def check_directories():
    logger.info("Checking directories...")
    
    directories = [
        'models',
        'models/model_history',
        'data/uploaded/images',
        'data/uploaded/documents',
        'data/uploaded/drawings',
        'data/custom_dataset',
        'data/exports',
        'static',
        'static/css',
        'static/images',
        'templates',
        'logs'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    logger.info("All directories are ready")
    return True