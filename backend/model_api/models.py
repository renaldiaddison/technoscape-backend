import os
import tensorflow as tf
from utils import utils

class Model:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._load_model()
        return cls._instance

    @classmethod
    def _load_model(cls):
        model_path = utils.get_directory('RELATIVE_PATH')
        return tf.keras.models.load_model(model_path)
