import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
import os
import time
from datetime import datetime
import keras_tuner as kt
from utils import data_augmentor
from database import db_manager
from config import config

class AdvancedModelTrainer:
    def __init__(self):
        self.model = None
        self.history = None
        self.training_time = 0
    
    def load_data(self, use_augmentation=True):
       