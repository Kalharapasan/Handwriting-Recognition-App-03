#!/usr/bin/env python3

import requests
import base64
import json
import time
import sys
from io import BytesIO
from PIL import Image, ImageDraw
import numpy as np

BASE_URL = "http://localhost:8000"
TEST_USER_ID = 1

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    print(f"{GREEN}✓ {message}{RESET}")

def print_error(message):
    print(f"{RED}✗ {message}{RESET}")

def print_info(message):
    print(f"{BLUE}ℹ {message}{RESET}")

def print_warning(message):
    print(f"{YELLOW}⚠ {message}{RESET}")
    
def create_test_digit_image(digit=5):
    img = Image.new('L', (28, 28), color=255)
    draw = ImageDraw.Draw(img)
    draw.text((8, 4), str(digit), fill=0)
    return img

def image_to_base64(img):
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    img_bytes = buffer.getvalue()
    return base64.b64encode(img_bytes).decode()

def test_health_check():
    print_info("Testing health check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check passed - Status: {data['status']}")
            print_info(f"  Model loaded: {data['model_loaded']}")
            return True
        else:
            print_error(f"Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Health check error: {str(e)}")
        return False

def test_model_status():
    print_info("Testing model status...")
    try:
        response = requests.get(f"{BASE_URL}/api/model/status")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Model status retrieved")
            print_info(f"  Model loaded: {data['model_loaded']}")
            print_info(f"  Model version: {data['model_version']}")
            return True
        else:
            print_error(f"Model status failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Model status error: {str(e)}")
        return False