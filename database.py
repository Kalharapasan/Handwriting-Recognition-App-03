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
    def __init__(self, db_url=None):
        self.db_url = db_url or config.DATABASE_URL
        self.engine = create_engine(self.db_url)
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        
    def add_user(self, username, email=None):
        user = User(username=username, email=email)
        self.session.add(user)
        self.session.commit()
        return user.id
    
    def add_prediction(self, user_id, predicted_digit, confidence, image_path, user_input_type, file_name, processing_time, image_size, model_version):
        prediction = PredictionHistory(
            user_id=user_id,
            predicted_digit=predicted_digit,
            confidence=confidence,
            image_path=image_path,
            user_input_type=user_input_type,
            file_name=file_name,
            processing_time=processing_time,
            image_size=image_size,
            model_version=model_version
        )
        self.session.add(prediction)
        self.session.commit()
        return prediction.id
    
    def add_feedback(self, prediction_id, user_id, actual_digit, correct_prediction,confidence_rating=None, comments="", suggested_improvement=""):
        feedback = UserFeedback(
            prediction_id=prediction_id,
            user_id=user_id,
            actual_digit=actual_digit,
            correct_prediction=correct_prediction,
            confidence_rating=confidence_rating,
            comments=comments,
            suggested_improvement=suggested_improvement
        )
        self.session.add(feedback)
        self.session.commit()
    
    def add_custom_dataset_entry(self, user_id, image_path, actual_digit,dataset_type='training', metadata=None):
        entry = CustomDataset(
            user_id=user_id,
            image_path=image_path,
            actual_digit=actual_digit,
            dataset_type=dataset_type,
            metadata=metadata or {}
        )
        self.session.add(entry)
        self.session.commit()
        return entry.id
    
    def get_user_stats(self, user_id):
        predictions = self.session.query(PredictionHistory).filter_by(user_id=user_id).all()
        feedbacks = self.session.query(UserFeedback).filter_by(user_id=user_id).all()
        
        if not predictions:
            return None

        total_predictions = len(predictions)
        avg_confidence = np.mean([p.confidence for p in predictions])
        avg_processing_time = np.mean([p.processing_time for p in predictions])
        if feedbacks:
            correct_predictions = sum(1 for f in feedbacks if f.correct_prediction)
            user_accuracy = correct_predictions / len(feedbacks)
        else:
            user_accuracy = 0
        
        digit_counts = {}
        for p in predictions:
            digit_counts[p.predicted_digit] = digit_counts.get(p.predicted_digit, 0) + 1
        most_common_digit = max(digit_counts.items(), key=lambda x: x[1])[0] if digit_counts else None
        
        return {
            'total_predictions': total_predictions,
            'user_accuracy': user_accuracy,
            'average_confidence': avg_confidence,
            'average_processing_time': avg_processing_time,
            'most_common_digit': most_common_digit,
            'feedback_count': len(feedbacks)
        }
        
    
    def get_system_analytics(self):
        total_users = self.session.query(User).count()
        active_users = self.session.query(User).filter_by(is_active=True).count()
        total_predictions = self.session.query(PredictionHistory).count()
        recent_predictions = self.session.query(PredictionHistory).filter(
            PredictionHistory.timestamp >= datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        ).count()
        feedbacks = self.session.query(UserFeedback).all()
        if feedbacks:
            system_accuracy = sum(1 for f in feedbacks if f.correct_prediction) / len(feedbacks)
        else:
            system_accuracy = 0
        digit_stats = self.session.query(
            PredictionHistory.predicted_digit,
            func.count(PredictionHistory.id)
        ).group_by(PredictionHistory.predicted_digit).all()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'total_predictions': total_predictions,
            'today_predictions': recent_predictions,
            'system_accuracy': system_accuracy,
            'digit_distribution': dict(digit_stats)
        }
        
    
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

db_manager = AdvancedDatabaseManager()
    