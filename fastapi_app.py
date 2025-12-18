from fastapi import FastAPI, File, UploadFile, HTTPException, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import numpy as np
import cv2
from PIL import Image
import io
import base64
import os
import time
from datetime import datetime
import logging

from database import db_manager, AdvancedDatabaseManager
from utils import AdvancedImagePreprocessor, AdvancedModelManager, OCRProcessor, DataAugmentor
from model_trainer import AdvancedModelTrainer
from config import config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)