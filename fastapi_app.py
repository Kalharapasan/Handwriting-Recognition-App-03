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
    
@app.get("/", response_class=HTMLResponse)
async def root():
    try:
        with open("/home/claude/templates/index.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
            <head><title>HWR System</title></head>
            <body>
                <h1>Handwriting Recognition System</h1>
                <p>Loading interface...</p>
                <script>window.location.href = '/dashboard';</script>
            </body>
        </html>
        """

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard():
    try:
        with open("/home/claude/templates/dashboard.html", "r") as f:
            return f.read()
    except FileNotFoundError:
        return HTMLResponse(content="<h1>Dashboard loading...</h1>")

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "model_loaded": model_manager.model is not None,
        "database_connected": True,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/predict")
async def predict_digit(request: PredictionRequest):
    try:
        start_time = time.time()
        image_data = base64.b64decode(request.image_data.split(',')[1] if ',' in request.image_data else request.image_data)
        image = Image.open(io.BytesIO(image_data))
        image_np = np.array(image)
        
        processed_image, processing_time = image_preprocessor.preprocess_image(
            image_np, 
            target_size=(28, 28),
            enhancement_level=request.enhancement_level
        )
        
        processed_image = processed_image.reshape(1, 28, 28, 1)
        
        predicted_digit, confidence, result = model_manager.predict_digit(
            processed_image, 
            return_all=True
        )
        
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    