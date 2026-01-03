"""
YOLO model initialization and management
"""
from ultralytics import YOLO
from config import MODEL_PATH


class SafetyDetectionModel:
    """Wrapper class for YOLO model"""
    
    def __init__(self):
        """Initialize the YOLO model"""
        print("Loading AI model...")
        self.model = YOLO(MODEL_PATH)
        print("Model loaded successfully!")
    
    def detect(self, frame):
        """
        Run detection on a frame
        
        Args:
            frame: Input image frame
        
        Returns:
            Detection results from YOLO
        """
        return self.model(frame)
    
    def get_class_name(self, class_id):
        """Get class name by ID"""
        return self.model.names[class_id]


# Global model instance
model = None


def get_model():
    """Get or create the global model instance"""
    global model
    if model is None:
        model = SafetyDetectionModel()
    return model
