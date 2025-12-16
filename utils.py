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