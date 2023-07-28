import os
import tensorflow as tf
from utils import utils
from joblib import load
from technoscape_backend.settings import BASE_DIR

class Model:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._load_model()
        return cls._instance

    @classmethod
    def _load_model(cls):
        model_path = BASE_DIR / 'model_api' / 'logistic_regression_model.pkl'
        return tf.keras.models.load_model(model_path)
