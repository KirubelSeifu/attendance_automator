"""
Attendance processing logic
Chapter 1: Foundation - Business Rules
"""
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class AttendanceStatus(Enum):
    """Attendance recognition states"""
    DETECTING = "Detecting..."
    VERIFIED = "✓ Attendance Marked"
    ALREADY_MARKED = "Already marked today"
    UNKNOWN = "Unknown face"
    ERROR = "Error"

@dataclass
class RecognitionResult:
    """Structured recognition result"""
    student_id: int
    name: str
    confidence: float
    status: AttendanceStatus
    message: str

class AttendanceProcessor:
    """
    Handles attendance logic and business rules
    Single responsibility: Process attendance decisions
    """
    
    def __init__(self, database):
        self.db = database
        self.verification_cache = {}  # student_id -> attempt_count
    
    def process_recognition(self, student_id: int, confidence: float) -> RecognitionResult:
        """
        Process a recognition result and decide attendance action
        Returns: RecognitionResult with status
        """
        if not student_id or confidence > 50:  # Unknown
            return RecognitionResult(
                student_id=0,
                name="Unknown",
                confidence=confidence,
                status=AttendanceStatus.UNKNOWN,
                message="Face not recognized"
            )
        
        # Get student info
        name = self.db.get_student_name(student_id)
        if not name:
            return RecognitionResult(
                student_id=student_id,
                name="Unknown",
                confidence=confidence,
                status=AttendanceStatus.ERROR,
                message="Student not found in database"
            )
        
        # Check if already marked today
        today = datetime.now().strftime('%Y-%m-%d')
        if self.db.is_attendance_marked(student_id, today):
            return RecognitionResult(
                student_id=student_id,
                name=name,
                confidence=confidence,
                status=AttendanceStatus.ALREADY_MARKED,
                message="Attendance already recorded today"
            )
        
        # Increment verification attempts
        self.verification_cache[student_id] = self.verification_cache.get(student_id, 0) + 1
        
        if self.verification_cache[student_id] >= 3:
            # Mark attendance after 3 successful recognitions
            if self.db.mark_attendance(student_id, name):
                # Clear cache after marking
                self.verification_cache.pop(student_id, None)
                return RecognitionResult(
                    student_id=student_id,
                    name=name,
                    confidence=confidence,
                    status=AttendanceStatus.VERIFIED,
                    message="Attendance marked successfully!"
                )
        
        # Still verifying
        return RecognitionResult(
            student_id=student_id,
            name=name,
            confidence=confidence,
            status=AttendanceStatus.DETECTING,
            message=f"Verifying... ({self.verification_cache[student_id]}/3)"
        )