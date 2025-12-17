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

