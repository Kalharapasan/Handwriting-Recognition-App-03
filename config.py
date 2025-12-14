import os
from datetime import datetime
class Config:
    DATABASE_URL = 'sqlite:///db.db'
    MODEL_PATH = 'models/handwriting_model.h5'
    UPLOAD_FOLDER = 'data/uploaded'
    CUSTOM_DATASET_PATH = 'data/custom_dataset'
    STATIC_FOLDER = 'static'