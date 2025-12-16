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
    
    @staticmethod
    def _custom_preprocessing(image, target_size, enhancement_level):
        pil_image = Image.fromarray(image)
        enhancer = ImageEnhance.Contrast(pil_image)
        pil_image = enhancer.enhance(enhancement_level)
        enhancer = ImageEnhance.Sharpness(pil_image)
        pil_image = enhancer.enhance(1.5)
        image = np.array(pil_image)
        image = cv2.resize(image, target_size)
        _, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        image = image.astype('float32') / 255.0
        return image
    
    @staticmethod
    def extract_digits_from_image(image_path, method='contour'):
        image = cv2.imread(image_path)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if method == 'contour':
            return AdvancedImagePreprocessor._extract_by_contour(gray)
        elif method == 'connected_components':
            return AdvancedImagePreprocessor._extract_by_connected_components(gray)
        else:
            return AdvancedImagePreprocessor._extract_by_projection(gray)
    
    @staticmethod
    def _extract_by_contour(gray_image):
        _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        digit_images = []
        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if 20 < w < 200 and 20 < h < 200:
                digit = gray_image[y:y+h, x:x+w]
                digit_images.append({
                    'image': digit,
                    'bbox': (x, y, w, h),
                    'area': w * h
                })
        digit_images.sort(key=lambda x: x['bbox'][0])
        return [d['image'] for d in digit_images]
    
    @staticmethod
    def _extract_by_connected_components(gray_image):
        _, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(thresh, connectivity=8)
        digit_images = []
        for i in range(1, num_labels):  # Skip background
            x = stats[i, cv2.CC_STAT_LEFT]
            y = stats[i, cv2.CC_STAT_TOP]
            w = stats[i, cv2.CC_STAT_WIDTH]
            h = stats[i, cv2.CC_STAT_HEIGHT]
            area = stats[i, cv2.CC_STAT_AREA]
            
            if 100 < area < 5000:  # Reasonable digit size
                digit = gray_image[y:y+h, x:x+w]
                digit_images.append(digit)
        
        return digit_images
    
    @staticmethod
    def deskew_image(image):
        coords = np.column_stack(np.where(image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, 
                               borderMode=cv2.BORDER_REPLICATE)
        
        return rotated

class AdvancedModelManager:
    def __init__(self, model_path=None):
        self.model = None
        self.model_version = "v2.0"
        self.performance_history = []
        self.load_model(model_path)
        
    def load_model(self, model_path):
        try:
            if model_path and os.path.exists(model_path):
                self.model = keras.models.load_model(model_path)
                logger.info(f"Model loaded successfully from {model_path}")
            else:
                logger.warning("No model found. Please train a model first.")
                self.model = None
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            self.model = None
    
    def predict_digit(self, image, return_all=False):
        if self.model is None:
            return 0, 0.0, {}
        
        start_time = time.time()
