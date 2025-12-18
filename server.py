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

def check_templates():
    logger.info("Checking templates...")
    
    template_path = 'templates/index.html'
    
    if os.path.exists(template_path):
        logger.info(" Templates found")
        return True
    else:
        logger.warning(f" Template not found at {template_path}")
        logger.info("Creating basic template...")
        
    os.makedirs('templates', exist_ok=True)
    with open(template_path, 'w') as f:
            f.write("""
<!DOCTYPE html>
<html>
<head>
    <title>Handwriting Recognition System</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>Handwriting Recognition System</h1>
    <p>The system is running. Access the API documentation at <a href="/docs">/docs</a></p>
</body>
</html>
            """)
        
    logger.info(" Basic template created")
    return True

def run_server(host='0.0.0.0', port=8000, reload=True):
    logger.info(f"Starting FastAPI server on {host}:{port}")
    logger.info(f"Reload mode: {reload}")
    logger.info("-" * 60)
    logger.info(f"Application will be available at:")
    logger.info(f"  - Local:   http://localhost:{port}")
    logger.info(f"  - Network: http://{host}:{port}")
    logger.info(f"  - API Docs: http://localhost:{port}/docs")
    logger.info(f"  - ReDoc:    http://localhost:{port}/redoc")
    logger.info("-" * 60)
    
    try:
        import uvicorn
        from fastapi_app import app
        
        uvicorn.run(
            "fastapi_app:app",
            host=host,
            port=port,
            reload=reload,
            log_level="info"
        )
    except KeyboardInterrupt:
        logger.info("\nServer stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        sys.exit(1)

def main():
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║   Advanced Handwriting Recognition System - FastAPI      ║
    ║                  Starting Application...                  ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    checks = [
        ("Dependencies", check_dependencies),
        ("Directories", check_directories),
        ("Templates", check_templates),
        ("Database", initialize_database),
        ("Model", check_model),
    ]
    
    for check_name, check_func in checks:
        if not check_func():
            logger.error(f" {check_name} check failed")
            logger.info("Please fix the above issues and try again")
            sys.exit(1)
    
    logger.info("\n All checks passed! Starting server...\n")