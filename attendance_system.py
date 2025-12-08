import cv2
import sys
class FaceDetector:
    def __init__(self):
        """Initialize the face detector with pre-trained model"""
        # Load the pre-trained face detection model from OpenCV
        cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        self.face_cascade = cv2.CascadeClassifier(cascade_path)
        
        if self.face_cascade.empty():
            raise IOError(f"Cannot load cascade classifier from {cascade_path}")
        
    def detect_faces(self, frame):
        """Detect faces in a single frame"""
        # Convert to grayscale (better for face detection)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        
        return faces
    
    def draw_face_boxes(self, frame, faces):
        """Draw rectangles around detected faces"""
        for (x, y, w, h) in faces:
            # Draw green rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            # Add label
            cv2.putText(frame, 'Face', (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        return frame

def main():
    """Main function to run the face detector"""
    print("Starting Face Detection System...")
    print("Press 'q' to quit the application.")
    
    # Initialize detector
    try:
        detector = FaceDetector()
    except IOError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    # Initialize camera (0 is usually the default webcam)
    camera = cv2.VideoCapture(0)
    
    if not camera.isOpened():
        print("ERROR: Could not open camera!")
        sys.exit(1)
    
    # Set camera resolution
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    print("\nCamera initialized successfully!")
    print("Faces will be marked with green boxes.")
    
    while True:
        # Capture frame-by-frame
        ret, frame = camera.read()
        
        if not ret:
            print("ERROR: Could not read frame from camera!")
            break
        
        # Detect faces
        faces = detector.detect_faces(frame)
        
        # Draw boxes around faces
        if len(faces) > 0:
            frame = detector.draw_face_boxes(frame, faces)
            status = f"Faces detected: {len(faces)}"
        else:
            status = "No faces detected"
        
        # Display status on frame
        cv2.putText(frame, status, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        # Display instructions
        cv2.putText(frame, "Press 'q' to quit", (10, frame.shape[0] - 10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
        
        # Display the resulting frame
        cv2.imshow('Face Detection', frame)
        
        # Break the loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    camera.release()
    cv2.destroyAllWindows()
    print("\nFace detection system stopped.")

if __name__ == "__main__":
    main()