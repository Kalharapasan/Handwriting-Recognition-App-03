import os
from datetime import datetime
class Config:
    DATABASE_URL = 'sqlite:///db.db'
    MODEL_PATH = 'models/handwriting_model.h5'
    UPLOAD_FOLDER = 'data/uploaded'
    CUSTOM_DATASET_PATH = 'data/custom_dataset'
    STATIC_FOLDER = 'static'
    IMG_HEIGHT = 28
    IMG_WIDTH = 28
    BATCH_SIZE = 32
    EPOCHS = 1
    MAX_FILE_SIZE = 50 * 1024 * 1024  
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp', 'pdf', 'txt'}
    ENABLE_REAL_TIME_TRAINING = True
    ENABLE_MULTI_USER = True
    ENABLE_ADVANCED_ANALYTICS = True
    
    @staticmethod
    def get_timestamp():
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def create_directories():
        """Create necessary directories"""
        directories = [
            'models/model_history',
            'data/uploaded/images',
            'data/uploaded/documents',
            'data/uploaded/drawings',
            'data/custom_dataset',
            'static/css',
            'static/images'
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
config = Config()
config.create_directories()