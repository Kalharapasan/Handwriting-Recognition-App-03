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
        (x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data
        x_train = x_train.astype('float32') / 255.0
        x_test = x_test.astype('float32') / 255.0
        x_train = x_train.reshape(-1, 28, 28, 1)
        x_test = x_test.reshape(-1, 28, 28, 1)
        y_train_cat = keras.utils.to_categorical(y_train, 10)
        y_test_cat = keras.utils.to_categorical(y_test, 10)
        
        if use_augmentation:
            x_train_augmented = []
            y_train_augmented = []
            
            for i in range(len(x_train)):
                x_train_augmented.append(x_train[i])
                y_train_augmented.append(y_train_cat[i])
                for _ in range(2):  
                    augmented_img = data_augmentor.augment_image(x_train[i].reshape(28, 28))
                    x_train_augmented.append(augmented_img.reshape(28, 28, 1))
                    y_train_augmented.append(y_train_cat[i])
            
            x_train = np.array(x_train_augmented)
            y_train_cat = np.array(y_train_augmented)
        
        return (x_train, y_train_cat), (x_test, y_test_cat)
    
    def create_advanced_model(self, hp=None):
        if hp:
            filters_1 = hp.Int('filters_1', 32, 128, step=32)
            filters_2 = hp.Int('filters_2', 64, 256, step=64)
            dense_units = hp.Int('dense_units', 128, 512, step=128)
            learning_rate = hp.Choice('learning_rate', [1e-2, 1e-3, 1e-4])
            dropout_rate = hp.Float('dropout_rate', 0.2, 0.5, step=0.1)
        else:
            filters_1 = 64
            filters_2 = 128
            dense_units = 256
            learning_rate = 1e-3
            dropout_rate = 0.3
        model = keras.Sequential([
            layers.Conv2D(filters_1, (3, 3), activation='relu', input_shape=(28, 28, 1)),
            layers.BatchNormalization(),
            layers.Conv2D(filters_1, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(dropout_rate),
        ])