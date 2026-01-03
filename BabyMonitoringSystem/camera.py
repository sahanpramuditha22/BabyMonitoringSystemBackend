"""
Camera and frame generation logic
"""
import time
import cv2
from detection import DetectionProcessor
from models import get_model
from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    FRAME_DELAY
)


class CameraHandler:
    """Handles camera input and frame generation"""
    
    def __init__(self):
        """Initialize the camera handler"""
        self.detection = DetectionProcessor()
        self.model = get_model()
        self.cap = None
    
    def initialize_camera(self):
        """Initialize camera capture"""
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        print("Camera started...")
    
    def generate_frames(self):
        """
        Generate video frames with object detection and distance calculation
        
        Yields:
            bytes: JPEG encoded frame with detection overlay
        """
        if self.cap is None:
            self.initialize_camera()
        
        while True:
            success, frame = self.cap.read()
            if not success:
                print("Camera error!")
                break
            
            # Run object detection
            results = self.model.detect(frame)
            
            # Extract detections
            baby_boxes, hazard_boxes = self.detection.extract_detections(results)
            
            # Start with basic annotated frame
            annotated = results[0].plot()
            
            # Process distances and get alerts
            distance_data, frame_has_critical = self.detection.process_distances(
                baby_boxes, hazard_boxes
            )
            
            # Draw distance lines and labels
            for data in distance_data:
                color = data['color']
                baby_center = data['baby_center']
                hazard_center = data['hazard_center']
                distance = data['distance']
                alert_level = data['alert_level']
                hazard_box = data['hazard_box']
                
                # Draw line between baby and hazard
                cv2.line(annotated, baby_center, hazard_center, color, 2)
                
                # Draw distance text
                mid_point = (
                    (baby_center[0] + hazard_center[0]) // 2,
                    (baby_center[1] + hazard_center[1]) // 2
                )
                cv2.putText(annotated, f"{distance:.1f}px", 
                           (mid_point[0], mid_point[1] - 10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
                
                # Draw alert level on hazard box
                x1, y1, x2, y2 = map(int, hazard_box)
                cv2.putText(annotated, f"{alert_level}", 
                           (x1, y1 - 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
            
            # Add status overlay
            status_text = f"Baby: {len(baby_boxes)} | Hazards: {len(hazard_boxes)} | Critical: {len(self.detection.current_critical_alerts)}"
            cv2.putText(annotated, status_text, (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # Add warning if critical alerts
            if frame_has_critical:
                warning_text = f"🚨 {len(self.detection.current_critical_alerts)} CRITICAL ALERT(S)!"
                cv2.putText(annotated, warning_text, (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
            
            # Add timestamp
            timestamp = time.strftime("%H:%M:%S")
            cv2.putText(annotated, timestamp, (annotated.shape[1] - 120, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # Encode frame to JPEG
            ret, buffer = cv2.imencode('.jpg', annotated)
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
            # Small delay
            time.sleep(FRAME_DELAY)
    
    def cleanup(self):
        """Clean up camera resources"""
        if self.cap:
            self.cap.release()


# Global camera handler instance
camera_handler = None


def get_camera_handler():
    """Get or create the global camera handler instance"""
    global camera_handler
    if camera_handler is None:
        camera_handler = CameraHandler()
    return camera_handler
