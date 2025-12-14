import sqlite3
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, Text, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import ForeignKey
from datetime import datetime
import json
import numpy as np
from config import config

Base = declarative_base()
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(200), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

class PredictionHistory(Base):
    __tablename__ = 'prediction_history'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    predicted_digit = Column(Integer)
    confidence = Column(Float)
    image_path = Column(String(500))
    user_input_type = Column(String(50))
    file_name = Column(String(255))
    processing_time = Column(Float)
    image_size = Column(String(50))
    model_version = Column(String(100))
    
    user = relationship("User", back_populates="predictions")

class UserFeedback(Base):
    __tablename__ = 'user_feedback'
    
    id = Column(Integer, primary_key=True)
    prediction_id = Column(Integer, ForeignKey('prediction_history.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    actual_digit = Column(Integer)
    correct_prediction = Column(Boolean)
    confidence_rating = Column(Integer)  
    comments = Column(Text)
    suggested_improvement = Column(Text)

class ModelPerformance(Base):
    __tablename__ = 'model_performance'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    accuracy = Column(Float)
    loss = Column(Float)
    validation_accuracy = Column(Float)
    validation_loss = Column(Float)
    training_time = Column(Float)
    model_architecture = Column(Text)
    hyperparameters = Column(JSON)

class CustomDataset(Base):
    __tablename__ = 'custom_dataset'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    timestamp = Column(DateTime, default=datetime.utcnow)
    image_path = Column(String(500))
    actual_digit = Column(Integer)
    is_verified = Column(Boolean, default=False)
    dataset_type = Column(String(50))  
    metadata = Column(JSON)

class SystemLog(Base):
    __tablename__ = 'system_logs'
    
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    log_level = Column(String(20))  
    module = Column(String(100))
    message = Column(Text)
    user_id = Column(Integer, ForeignKey('users.id'))

User.predictions = relationship("PredictionHistory", order_by=PredictionHistory.id, back_populates="user")

class AdvancedDatabaseManager:
    
    def get_system_analytics(self):
        
    
    def export_user_data(self, user_id, format='csv'):
        predictions = self.session.query(PredictionHistory).filter_by(user_id=user_id).all()
        feedbacks = self.session.query(UserFeedback).filter_by(user_id=user_id).all()
        
        prediction_data = []
        for p in predictions:
            prediction_data.append({
                'timestamp': p.timestamp,
                'predicted_digit': p.predicted_digit,
                'confidence': p.confidence,
                'input_type': p.user_input_type,
                'processing_time': p.processing_time
            })
        
        feedback_data = []
        for f in feedbacks:
            feedback_data.append({
                'timestamp': f.timestamp,
                'actual_digit': f.actual_digit,
                'correct_prediction': f.correct_prediction,
                'confidence_rating': f.confidence_rating,
                'comments': f.comments
            })
        
        if format == 'csv':
            pred_df = pd.DataFrame(prediction_data)
            feedback_df = pd.DataFrame(feedback_data)
            return pred_df, feedback_df
        elif format == 'json':
            return {
                'predictions': prediction_data,
                'feedbacks': feedback_data
            }
    
    def log_system_event(self, log_level, module, message, user_id=None):
        log = SystemLog(
            log_level=log_level,
            module=module,
            message=message,
            user_id=user_id
        )
        self.session.add(log)
        self.session.commit()
    