import logging
import sys
from flask import Flask, render_template, Response, jsonify
from datetime import datetime
from config import Config
from core.camera import FaceEngine
from core.database import Database

# FIX: Force UTF-8 for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(Config.LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize core components
config = Config()
db = Database(config)
face_engine = FaceEngine(config)

# Camera state
camera_initialized = False

def initialize_system():
    """Initialize system components on startup"""
    global camera_initialized
    
    logger.info("="*50)
    logger.info("FACE ATTENDANCE SYSTEM - CHAPTER 1")
    logger.info("="*50)
    
    # Initialize camera
    try:
        camera_initialized = face_engine.initialize_camera()
        if not camera_initialized:
            logger.error("Failed to initialize camera - system running in degraded mode")
        else:
            logger.info("[OK] Camera system ready")
    except Exception as e:
        logger.error(f"System initialization error: {e}")
        camera_initialized = False

@app.route('/')
def index():
    """Home page with live camera feed"""
    stats = db.get_today_stats()
    return render_template(
        'index.html',
        camera_ready=camera_initialized,
        stats=stats,
        current_time=datetime.now().strftime('%H:%M:%S')
    )

@app.route('/video_feed')
def video_feed():
    """Video streaming route"""
    if not camera_initialized:
        logger.warning("Camera not initialized - streaming error frames")
    
    return Response(
        face_engine.generate_frames(),
        mimetype='multipart/x-mixed-replace; boundary=frame',
        headers={
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Expires': '0'
        }
    )

@app.route('/api/stats')
def api_stats():
    """API endpoint for real-time stats"""
    return jsonify(db.get_today_stats())

@app.route('/health')
def health_check():
    """System health check"""
    return jsonify({
        'status': 'healthy' if camera_initialized else 'degraded',
        'camera': camera_initialized,
        'database': db.db_path.exists()
    })

@app.errorhandler(500)
def internal_error(error):
    """Handle internal server errors"""
    logger.error(f"Server Error: {error}")
    return render_template('errors/500.html'), 500

@app.errorhandler(404)
def not_found_error(error):
    """Handle not found errors"""
    return render_template('errors/404.html'), 404

if __name__ == '__main__':
    initialize_system()
    
    logger.info("Starting Flask server...")
    logger.info("Access the application at http://127.0.0.1:5000")
    
    try:
        app.run(
            debug=False,
            host='0.0.0.0',
            port=5000,
            threaded=True,
            use_reloader=False
        )
    finally:
        # Cleanup
        face_engine.release_camera()
        logger.info("[OK] System shutdown complete")

import atexit

def cleanup():
    logger.info("[OK] Cleanup: Releasing camera")
    face_engine.release_camera()

atexit.register(cleanup)