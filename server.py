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

def check_model():
    logger.info("Checking for trained model...")
    
    model_path = 'models/handwriting_model.h5'
    
    if os.path.exists(model_path):
        logger.info(f" Model found at {model_path}")
        return True
    else:
        logger.warning(f"⚠ No model found at {model_path}")
        logger.info("You can train a model using the /api/train endpoint or by running:")
        logger.info(" python model_trainer.py")
        return True 

def initialize_database():
    logger.info("Initializing database...")
    
    try:
        from database import db_manager
        logger.info(" Database initialized successfully")
        return True
    except Exception as e:
        logger.error(f" Database initialization failed: {str(e)}")
        return False