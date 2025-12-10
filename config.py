"""
Configuration module for Face Attendance System
"""
import os
import cv2
from pathlib import Path

class Config:
    """Base configuration"""
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'super_secret_key_for_session_change_in_production')
    
    # Paths
    BASE_DIR = Path(__file__).parent
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    TRAINING_DIR = UPLOAD_FOLDER / "training"
    PROFILE_DIR = UPLOAD_FOLDER / "profiles"
    MODEL_DIR = BASE_DIR / "models"
    LOG_DIR = BASE_DIR / "logs"
    
    # Ensure directories exist
    TRAINING_DIR.mkdir(parents=True, exist_ok=True)
    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    # File paths
    DATABASE = BASE_DIR / "attendance.db"
    MODEL_FILE = MODEL_DIR / "face_model.yml"
    HAAR_CASCADE = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    
    # Camera
    CAMERA_INDEX = int(os.getenv('CAMERA_INDEX', 0))
    CAMERA_WIDTH = int(os.getenv('CAMERA_WIDTH', 640))
    CAMERA_HEIGHT = int(os.getenv('CAMERA_HEIGHT', 480))
    CAMERA_FPS = int(os.getenv('CAMERA_FPS', 30))
    
    # Face Detection
    FACE_SCALE_FACTOR = 1.3
    FACE_MIN_NEIGHBORS = 5
    FACE_MIN_SIZE = (30, 30)
    
    # Recognition
    CONFIDENCE_THRESHOLD = 50
    VERIFICATION_ATTEMPTS = 3
    
    # Logging
    LOG_FILE = LOG_DIR / "app.log"
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE = Config.BASE_DIR / "test.db"

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}