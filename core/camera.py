"""
Face detection and camera management module
Chapter 1: Foundation & Detection - Core Component
"""
import cv2
import numpy as np
import logging
from config import Config
from pathlib import Path

logger = logging.getLogger(__name__)

class CameraError(Exception):
    """Custom exception for camera-related errors"""
    pass

class FaceEngine:
    """
    Handles camera operations and face detection
    Single responsibility: Manage video feed and detect faces
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.camera = None
        self.face_cascade = None
        self._initialize_face_detector()
        logger.info("FaceEngine initialized")
    
    def _initialize_face_detector(self):
        """Initialize Haar Cascade face detector"""
        cascade_path = Path(self.config.HAAR_CASCADE)
        if not cascade_path.exists():
            logger.error(f"Haar cascade not found at {cascade_path}")
            raise FileNotFoundError(f"Haar cascade file missing: {cascade_path}")
        
        self.face_cascade = cv2.CascadeClassifier(str(cascade_path))
        logger.info("Face detector initialized successfully")
    
    def initialize_camera(self) -> bool:
        """
        Initialize camera with multiple fallback indices
        Returns: True if successful, False otherwise
        """
        # Try different camera indices
        indices_to_try = [
            self.config.CAMERA_INDEX,
            1, 2, -1  # Common alternatives
        ]
        
        for idx in indices_to_try:
            try:
                logger.info(f"Attempting camera at index {idx}")
                self.camera = cv2.VideoCapture(idx, cv2.CAP_DSHOW)
                
                if self.camera.isOpened():
                    # Configure camera
                    self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.config.CAMERA_WIDTH)
                    self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.config.CAMERA_HEIGHT)
                    self.camera.set(cv2.CAP_PROP_FPS, self.config.CAMERA_FPS)
                    
                    # Warm up camera
                    for _ in range(10):
                        self.camera.read()
                    
                    logger.info(f"✓ Camera initialized at index {idx}")
                    return True
                else:
                    self.camera.release()
                    
            except Exception as e:
                logger.warning(f"Failed to open camera at index {idx}: {e}")
                if self.camera:
                    self.camera.release()
        
        logger.error("❌ Could not initialize any camera")
        return False
    
    def is_camera_ready(self) -> bool:
        """Check if camera is initialized and ready"""
        return self.camera is not None and self.camera.isOpened()
    
    def release_camera(self):
        """Safely release camera resources"""
        if self.camera:
            self.camera.release()
            logger.info("Camera released")
            self.camera = None
    
    def detect_faces(self, frame: np.ndarray) -> tuple:
        """
        Detect faces in a frame
        Returns: Tuple of (faces_list, grayscale_frame)
        """
        try:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=self.config.FACE_SCALE_FACTOR,
                minNeighbors=self.config.FACE_MIN_NEIGHBORS,
                minSize=self.config.FACE_MIN_SIZE
            )
            return faces, gray
        except Exception as e:
            logger.error(f"Face detection error: {e}")
            return [], cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    def draw_face_boxes(self, frame: np.ndarray, faces: list) -> np.ndarray:
        """
        Draw detection boxes on frame
        Returns: Annotated frame
        """
        annotated = frame.copy()
        
        for (x, y, w, h) in faces:
            # Draw rectangle
            cv2.rectangle(annotated, (x, y), (x+w, y+h), (0, 255, 0), 2)
            
            # Add label
            label = "Face Detected"
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            thickness = 1
            
            # Get text size for background
            (text_width, text_height), baseline = cv2.getTextSize(
                label, font, font_scale, thickness
            )
            
            # Draw text background
            cv2.rectangle(
                annotated,
                (x, y - text_height - 10),
                (x + text_width, y),
                (0, 255, 0),
                cv2.FILLED
            )
            
            # Draw text
            cv2.putText(
                annotated,
                label,
                (x, y - 5),
                font,
                font_scale,
                (0, 0, 0),
                thickness
            )
        
        return annotated
    
    def _encode_frame(self, frame: np.ndarray) -> bytes:
        """Encode frame for web streaming"""
        try:
            ret, buffer = cv2.imencode(
                '.jpg',
                frame,
                [cv2.IMWRITE_JPEG_QUALITY, 85]
            )
            if not ret:
                logger.error("Frame encoding failed")
                return b''
            
            return b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + \
                   buffer.tobytes() + b'\r\n'
        except Exception as e:
            logger.error(f"Frame encoding error: {e}")
            return b''
    
    def generate_frames(self):
        """
        Main generator for video feed
        Yields: Encoded frame bytes
        """
        if not self.is_camera_ready():
            logger.error("Camera not ready, generating error frames")
            # Generate error placeholder frames
            while True:
                frame = np.zeros(
                    (self.config.CAMERA_HEIGHT, self.config.CAMERA_WIDTH, 3),
                    dtype=np.uint8
                )
                
                # Error message
                message = "CAMERA NOT AVAILABLE"
                sub_message = "Check connection and permissions"
                
                # Center text
                font = cv2.FONT_HERSHEY_SIMPLEX
                text_size = cv2.getTextSize(message, font, 1, 2)[0]
                sub_size = cv2.getTextSize(sub_message, font, 0.5, 1)[0]
                
                text_x = (self.config.CAMERA_WIDTH - text_size[0]) // 2
                sub_x = (self.config.CAMERA_WIDTH - sub_size[0]) // 2
                
                cv2.putText(frame, message, (text_x, 200),
                           font, 1, (255, 255, 255), 2)
                cv2.putText(frame, sub_message, (sub_x, 250),
                           font, 0.5, (200, 200, 200), 1)
                
                yield self._encode_frame(frame)
                time.sleep(0.5)
                return  # Only show once
        
        frame_count = 0
        try:
            while True:
                success, frame = self.camera.read()
                if not success:
                    logger.warning("Failed to read frame")
                    break
                
                # Detect faces
                faces, gray = self.detect_faces(frame)
                
                # Draw boxes
                annotated_frame = self.draw_face_boxes(frame, faces)
                
                # Add status overlay
                status = f"Faces: {len(faces)} | FPS: ~{frame_count % 30}"
                cv2.putText(annotated_frame, status, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 1)
                
                yield self._encode_frame(annotated_frame)
                frame_count += 1
                
        except Exception as e:
            logger.error(f"Video stream error: {e}")
            self.release_camera()
        
        #finally:
            #self.release_camera()