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
    EPOCHS = 100