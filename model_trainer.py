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
            layers.Conv2D(filters_2, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.Conv2D(filters_2, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.MaxPooling2D((2, 2)),
            layers.Dropout(dropout_rate),
            layers.Conv2D(filters_2, (3, 3), activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(dropout_rate),
            layers.Flatten(),
            layers.Dense(dense_units, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(dropout_rate + 0.2),
            layers.Dense(dense_units // 2, activation='relu'),
            layers.Dropout(dropout_rate),
            layers.Dense(10, activation='softmax')
        ])
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
            loss='categorical_crossentropy',
            metrics=['accuracy', 'precision', 'recall']
        )
        
        return model
    
    def train_model(self, use_hyperparameter_tuning=False):
        start_time = time.time()
        (x_train, y_train), (x_test, y_test) = self.load_data(use_augmentation=True)
        if use_hyperparameter_tuning:
            tuner = kt.Hyperband(
                self.create_advanced_model,
                objective='val_accuracy',
                max_epochs=50,
                factor=3,
                directory='models/model_history',
                project_name='hyperparameter_tuning'
            )
            
            stop_early = tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=5)
            tuner.search(x_train, y_train, epochs=50, validation_split=0.2, callbacks=[stop_early])
            best_hps = tuner.get_best_hyperparameters(num_trials=1)[0]
            self.model = tuner.hypermodel.build(best_hps)
        else:
            self.model = self.create_advanced_model()
        
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_accuracy',
                patience=15,
                restore_best_weights=True,
                mode='max'
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=1e-7
            ),
            keras.callbacks.ModelCheckpoint(
                'models/best_model.h5',
                monitor='val_accuracy',
                save_best_only=True,
                mode='max'
            ),
            keras.callbacks.CSVLogger('models/training_history.csv'),
            keras.callbacks.TensorBoard(
                log_dir='models/tensorboard_logs',
                histogram_freq=1
            )
        ]
        
        datagen = keras.preprocessing.image.ImageDataGenerator(
            rotation_range=10,
            width_shift_range=0.1,
            height_shift_range=0.1,
            zoom_range=0.1,
            shear_range=0.1,
            fill_mode='nearest'
        )
        
        self.history = self.model.fit(
            datagen.flow(x_train, y_train, batch_size=config.BATCH_SIZE),
            epochs=config.EPOCHS,
            validation_data=(x_test, y_test),
            callbacks=callbacks,
            verbose=1
        )
        
        self.training_time = time.time() - start_time
        self.model.save(config.MODEL_PATH)
        self._log_training_performance(x_test, y_test)
        
        return self.history
    
    def _log_training_performance(self, x_test, y_test):
        test_loss, test_accuracy = self.model.evaluate(x_test, y_test, verbose=0)
        val_accuracy = max(self.history.history['val_accuracy'])
        
        performance_data = {
            'timestamp': datetime.utcnow(),
            'accuracy': test_accuracy,
            'loss': test_loss,
            'validation_accuracy': val_accuracy,
            'validation_loss': min(self.history.history['val_loss']),
            'training_time': self.training_time,
            'model_architecture': str(self.model.summary()),
            'hyperparameters': {
                'batch_size': config.BATCH_SIZE,
                'epochs': config.EPOCHS,
                'optimizer': 'Adam'
            }
        }
        
        print(f"Training completed in {self.training_time:.2f} seconds")
        print(f"Test Accuracy: {test_accuracy:.4f}")
        print(f"Validation Accuracy: {val_accuracy:.4f}")
        
    def evaluate_model(self, x_test, y_test):
        