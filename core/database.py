"""
Database management module
Chapter 1: Foundation - Data Persistence
"""
import sqlite3
import logging
from contextlib import contextmanager
from config import Config
from datetime import datetime

logger = logging.getLogger(__name__)

class DatabaseError(Exception):
    """Custom database exception"""
    pass

class Database:
    """
    Handles all database operations with connection pooling
    Single responsibility: Manage SQLite database
    """
    
    def __init__(self, config: Config):
        self.config = config
        self.db_path = config.DATABASE
        self.init_database()
        logger.info(f"Database initialized at {self.db_path}")
    
    @contextmanager
    def get_connection(self):
        """Context manager for safe DB connections"""
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            logger.error(f"Database connection error: {e}")
            raise DatabaseError(f"Database error: {e}")
        finally:
            if conn:
                conn.close()
    
    def init_database(self):
        """Create tables if they don't exist"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Students table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS students (
                    student_id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    first_name TEXT,
                    last_name TEXT,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1,
                    photo_path TEXT
                )
            ''')
            
            # Attendance table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS attendance (
                    attendance_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id INTEGER NOT NULL,
                    attendance_date DATE NOT NULL,
                    attendance_time TIME NOT NULL,
                    session_id TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (student_id) REFERENCES students (student_id),
                    UNIQUE(student_id, attendance_date)
                )
            ''')
            
            # System logs table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS system_logs (
                    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    module TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            conn.commit()
            logger.info("Database schema initialized")
    
    def get_today_stats(self) -> dict:
        """Get today's attendance statistics"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                # Today's count
                today = datetime.now().strftime('%Y-%m-%d')
                cursor.execute(
                    "SELECT COUNT(*) as count FROM attendance WHERE attendance_date = ?",
                    (today,)
                )
                today_count = cursor.fetchone()['count']
                
                # Total active students
                cursor.execute("SELECT COUNT(*) as count FROM students WHERE is_active = 1")
                total_students = cursor.fetchone()['count']
                
                return {
                    'today_count': today_count,
                    'total_students': total_students,
                    'attendance_rate': (today_count / total_students * 100) if total_students > 0 else 0
                }
        except Exception as e:
            logger.error(f"Stats fetch error: {e}")
            return {'today_count': 0, 'total_students': 0, 'attendance_rate': 0}
    
    def log_system_event(self, level: str, message: str, module: str = None):
        """Log system events to database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO system_logs (level, message, module) VALUES (?, ?, ?)",
                    (level, message, module)
                )
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to log system event: {e}")