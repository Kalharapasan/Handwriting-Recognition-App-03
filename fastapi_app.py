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

app = FastAPI(
    title="Advanced Handwriting Recognition API",
    description="AI-powered handwriting recognition system with FastAPI",
    version="2.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")
image_preprocessor = AdvancedImagePreprocessor()
model_manager = AdvancedModelManager(config.MODEL_PATH)
ocr_processor = OCRProcessor()

class PredictionRequest(BaseModel):
    image_data: str 
    user_id: int = 1
    enhancement_level: float = 1.0
    
class FeedbackRequest(BaseModel):
    prediction_id: int
    user_id: int
    actual_digit: int
    confidence_rating: Optional[int] = None
    comments: Optional[str] = ""

class UserCreate(BaseModel):
    username: str
    email: Optional[str] = None

class TrainingConfig(BaseModel):
    use_hyperparameter_tuning: bool = False
    use_augmentation: bool = True
    epochs: int = 50
    batch_size: int = 32
    
