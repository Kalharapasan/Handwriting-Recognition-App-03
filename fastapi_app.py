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
        
        image_path = save_prediction_image(image_np)
        prediction_id = db_manager.add_prediction(
            user_id=request.user_id,
            predicted_digit=int(predicted_digit),
            confidence=float(confidence),
            image_path=image_path,
            user_input_type="drawing",
            file_name="drawing.png",
            processing_time=processing_time,
            image_size=f"{image_np.shape[0]}x{image_np.shape[1]}",
            model_version=model_manager.model_version
        )
        
        total_time = time.time() - start_time
        
        return {
            "success": True,
            "prediction_id": prediction_id,
            "predicted_digit": int(predicted_digit),
            "confidence": float(confidence),
            "all_predictions": result['all_predictions'].tolist() if result['all_predictions'] is not None else None,
            "processing_time": processing_time,
            "total_time": total_time,
            "timestamp": datetime.now().isoformat()
        }
        
    
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.post("/api/predict-upload")
async def predict_from_upload(file: UploadFile = File(...),user_id: int = Form(1),enhancement_level: float = Form(1.0)):
    try:
        
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_np = np.array(image)
        
        processed_image, processing_time = image_preprocessor.preprocess_image(
            image_np,
            target_size=(28, 28),
            enhancement_level=enhancement_level
        )
        
        processed_image = processed_image.reshape(1, 28, 28, 1)
        
        predicted_digit, confidence, result = model_manager.predict_digit(
            processed_image,
            return_all=True
        )
        image_path = save_uploaded_file(file, contents)
        prediction_id = db_manager.add_prediction(
            user_id=user_id,
            predicted_digit=int(predicted_digit),
            confidence=float(confidence),
            image_path=image_path,
            user_input_type="upload",
            file_name=file.filename,
            processing_time=processing_time,
            image_size=f"{image_np.shape[0]}x{image_np.shape[1]}",
            model_version=model_manager.model_version
        )
        
        return {
            "success": True,
            "prediction_id": prediction_id,
            "predicted_digit": int(predicted_digit),
            "confidence": float(confidence),
            "all_predictions": result['all_predictions'].tolist() if result['all_predictions'] is not None else None,
            "filename": file.filename,
            "processing_time": processing_time
        }
    except Exception as e:
        logger.error(f"Upload prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/predict-batch")
async def predict_batch(files: List[UploadFile] = File(...), user_id: int = Form(1)):
    try:
        results = []
        
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            image_np = np.array(image)
        
        processed_image, processing_time = image_preprocessor.preprocess_image(
                image_np,
                target_size=(28, 28)
        )

        processed_image = processed_image.reshape(1, 28, 28, 1)
        predicted_digit, confidence, _ = model_manager.predict_digit(processed_image)
            
        results.append({
            "filename": file.filename,
            "predicted_digit": int(predicted_digit),
            "confidence": float(confidence),
            "processing_time": processing_time
        })
        
        return {
            "success": True,
            "total_files": len(files),
            "results": results
        }
        
    except Exception as e:
        logger.error(f"Batch prediction error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
async def add_feedback(feedback: FeedbackRequest):
    try:
        db_manager.add_feedback(
            prediction_id=feedback.prediction_id,
            user_id=feedback.user_id,
            actual_digit=feedback.actual_digit,
            correct_prediction=(feedback.actual_digit == feedback.prediction_id),
            confidence_rating=feedback.confidence_rating,
            comments=feedback.comments
        )
        
        return {
            "success": True,
            "message": "Feedback recorded successfully"
        }
        
    except Exception as e:
        logger.error(f"Feedback error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics/system")
async def get_system_analytics():
    try:
        analytics = db_manager.get_system_analytics()
        return {
            "success": True,
            "data": analytics
        }
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/user/{user_id}")
async def get_user_analytics(user_id: int):
    try:
        stats = db_manager.get_user_stats(user_id)
        
        if stats is None:
            return {
                "success": False,
                "message": "No data found for user"
            }
        
        return {
            "success": True,
            "data": stats
        }
        
    except Exception as e:
        logger.error(f"User analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/analytics/predictions")
async def get_prediction_history(limit: int = 100, user_id: Optional[int] = None):
    try:
        from sqlalchemy import desc
        from database import PredictionHistory
        
        query = db_manager.session.query(PredictionHistory)
        
        if user_id:
            query = query.filter(PredictionHistory.user_id == user_id)
        
        predictions = query.order_by(desc(PredictionHistory.timestamp)).limit(limit).all()
        
        results = []
        for pred in predictions:
            results.append({
                "id": pred.id,
                "timestamp": pred.timestamp.isoformat(),
                "predicted_digit": pred.predicted_digit,
                "confidence": pred.confidence,
                "user_input_type": pred.user_input_type,
                "processing_time": pred.processing_time
            })
        
        return {
            "success": True,
            "count": len(results),
            "data": results
        }
        
    except Exception as e:
        logger.error(f"Prediction history error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


