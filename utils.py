import numpy as np
import cv2
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import tensorflow as tf
from tensorflow import keras
import os
import time
from pdf2image import convert_from_path
import tempfile
import pytesseract
from scipy import ndimage
import imutils
from config import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AdvancedImagePreprocessor:
    @staticmethod
    def preprocess_image(image, target_size=(28, 28), enhancement_level=1.0):
        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        
        if enhancement_level == 1.0:
            image = AdvancedImagePreprocessor._basic_preprocessing(image, target_size)
        elif enhancement_level == 2.0:
            image = AdvancedImagePreprocessor._advanced_preprocessing(image, target_size)
        else:
            image = AdvancedImagePreprocessor._custom_preprocessing(image, target_size, enhancement_level)
        
        processing_time = time.time() - start_time
        logger.info(f"Image preprocessing completed in {processing_time:.3f}s")
        
        return image, processing_time
    
    @staticmethod
    def _basic_preprocessing(image, target_size):
        image = cv2.resize(image, target_size)
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        image = image.astype('float32') / 255.0
        return image
    
    @staticmethod
    def _advanced_preprocessing(image, target_size):
        image = cv2.medianBlur(image, 3)
        kernel = np.ones((2, 2), np.uint8)
        image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
        image = cv2.resize(image, target_size)
        image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 11, 2)
        image = image.astype('float32') / 255.0
        return image
        
        
    

    