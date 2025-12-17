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

def test_prediction_base64():
    print_info("Testing prediction (base64)...")
    try:
        img = create_test_digit_image(5)
        img_base64 = image_to_base64(img)
        response = requests.post(
            f"{BASE_URL}/api/predict",
            json={
                "image_data": f"data:image/png;base64,{img_base64}",
                "user_id": TEST_USER_ID,
                "enhancement_level": 1.0
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print_success(f"Prediction successful")
                print_info(f"  Predicted digit: {data['predicted_digit']}")
                print_info(f"  Confidence: {data['confidence']:.2%}")
                print_info(f"  Processing time: {data['processing_time']:.3f}s")
                return True
            else:
                print_error("Prediction returned success=False")
                return False
        else:
            print_error(f"Prediction failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Prediction error: {str(e)}")
        return False

def test_prediction_upload():
    print_info("Testing prediction (file upload)...")
    try:
        img = create_test_digit_image(7)
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        files = {'file': ('test_digit.png', buffer, 'image/png')}
        data = {'user_id': TEST_USER_ID}
        response = requests.post(
            f"{BASE_URL}/api/predict-upload",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            result = response.json()
            if result['success']:
                print_success(f"Upload prediction successful")
                print_info(f"  Predicted digit: {result['predicted_digit']}")
                print_info(f"  Confidence: {result['confidence']:.2%}")
                return True
            else:
                print_error("Upload prediction returned success=False")
                return False
        else:
            print_error(f"Upload prediction failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Upload prediction error: {str(e)}")
        return False
    
def test_system_analytics():
    print_info("Testing system analytics...")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/system")
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                analytics = data['data']
                print_success("System analytics retrieved")
                print_info(f"  Total users: {analytics['total_users']}")
                print_info(f"  Total predictions: {analytics['total_predictions']}")
                print_info(f"  System accuracy: {analytics['system_accuracy']:.2%}")
                return True
            else:
                print_error("Analytics returned success=False")
                return False
        else:
            print_error(f"Analytics failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Analytics error: {str(e)}")
        return False

def test_user_analytics():
    print_info("Testing user analytics...")
    try:
        response = requests.get(f"{BASE_URL}/api/analytics/user/{TEST_USER_ID}")
        
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                print_success("User analytics retrieved")
                stats = data['data']
                if stats:
                    print_info(f"  Total predictions: {stats['total_predictions']}")
                    print_info(f"  User accuracy: {stats['user_accuracy']:.2%}")
                else:
                    print_info("  No data for user yet (expected for new user)")
                return True
            else:
                print_warning("No analytics data for user (may be expected)")
                return True
        else:
            print_error(f"User analytics failed with status {response.status_code}")
            return False
    except Exception as e:
        print_error(f"User analytics error: {str(e)}")
        return False