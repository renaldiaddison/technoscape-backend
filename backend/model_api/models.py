import os
from utils import utils
from technoscape_backend.settings import BASE_DIR
import joblib

class Model:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls._load_model()
        return cls._instance

    @classmethod
    def _load_model(cls):
        model_path = utils.get_directory('logistic_regression_model.pkl')
        return joblib.load(model_path)
