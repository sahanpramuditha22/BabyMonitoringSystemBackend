"""
Detection logic and frame processing
"""
import time
import cv2
from models import get_model
from pose_analyzer import PoseAnalyzer
from config import (
    CONFIDENCE_THRESHOLD, 
    CRITICAL_DISTANCE, 
    WARNING_DISTANCE,
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
    FRAME_DELAY,
    ALERT_COOLDOWN
)
from utils import calculate_distance, get_current_timestamp_str


class DetectionProcessor:
    """Handles object detection and frame processing"""
    
    def __init__(self):
        """Initialize the detection processor"""
        self.model = get_model()
        self.pose_analyzer = PoseAnalyzer()
        self.last_alert_time = 0
        self.current_critical_alerts = []
        self.alerts_history = []
    
    def extract_detections(self, results):
        """
        Extract baby and hazard detections from YOLO results
        
        Args:
            results: YOLO detection results
        
        Returns:
            tuple: (baby_boxes, hazard_boxes)
        """
        baby_boxes = []
        hazard_boxes = []
        
        for result in results:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                bbox = box.xyxy[0].tolist()
                class_name = self.model.get_class_name(class_id)
                
                if class_name == 'baby' and confidence > CONFIDENCE_THRESHOLD:
                    baby_boxes.append(bbox)
                elif class_name != 'baby' and confidence > CONFIDENCE_THRESHOLD:
                    hazard_boxes.append({
                        'bbox': bbox,
                        'name': class_name,
                        'confidence': confidence
                    })
        
        return baby_boxes, hazard_boxes
    
    def process_distances(self, baby_boxes, hazard_boxes, reach_data=None):
        """
        Calculate distances and generate alerts with reach analysis
        
        Args:
            baby_boxes: List of baby bounding boxes
            hazard_boxes: List of hazard detections
            reach_data: Reach posture data from pose analyzer
        
        Returns:
            list: Distance data for drawing
        """
        current_time = time.time()
        distance_data = []
        
        # Clear critical alerts
        self.current_critical_alerts.clear()
        frame_has_critical = False
        
        for baby_box in baby_boxes:
            for hazard in hazard_boxes:
                hazard_box = hazard['bbox']
                distance, baby_center, hazard_center = calculate_distance(baby_box, hazard_box)
                
                # Calculate reach-based pre-alert score
                reach_score = 0
                if reach_data and reach_data['is_reaching']:
                    # Boost alert level if baby is actively reaching
                    hand_pos = reach_data['hand_position']
                    if hand_pos:
                        hand_to_hazard = calculate_distance(
                            [hand_pos[0], hand_pos[1], hand_pos[0], hand_pos[1]],
                            hazard_box
                        )[0]
                        # Reach score: closer hand to hazard = higher score
                        reach_score = max(0, (100 - hand_to_hazard) / 2)
                
                # Determine alert level based on distance + reach
                color = (0, 255, 0)  # Green (SAFE)
                alert_level = "SAFE"
                effective_distance = distance
                
                # Reduce effective distance if actively reaching
                if reach_data and reach_data['is_reaching']:
                    effective_distance = distance * 0.7  # 30% reduction due to active reach
                
                if effective_distance < CRITICAL_DISTANCE:  # CRITICAL
                    color = (0, 0, 255)  # Red
                    alert_level = "CRITICAL"
                    frame_has_critical = True
                    
                    # Store critical alert
                    alert_data = {
                        'type': 'CRITICAL',
                        'hazard': hazard['name'],
                        'distance': float(distance),
                        'reach_score': float(reach_score),
                        'timestamp': current_time,
                        'is_reaching': reach_data['is_reaching'] if reach_data else False,
                        'reaching_arm': reach_data['primary_arm'] if reach_data else None,
                        'message': self._build_alert_message('CRITICAL', hazard['name'], distance, reach_data),
                        'time_str': get_current_timestamp_str()
                    }
                    self.current_critical_alerts.append(alert_data)
                    self.alerts_history.append(alert_data)
                
                elif effective_distance < WARNING_DISTANCE:  # WARNING
                    color = (0, 165, 255)  # Orange
                    alert_level = "WARNING"
                    
                    # Pre-alert if actively reaching
                    if reach_data and reach_data['is_reaching']:
                        alert_data = {
                            'type': 'PRE-ALERT',
                            'hazard': hazard['name'],
                            'distance': float(distance),
                            'reach_score': float(reach_score),
                            'timestamp': current_time,
                            'is_reaching': True,
                            'reaching_arm': reach_data['primary_arm'],
                            'message': f"⚠️ PRE-ALERT: Baby reaching with {reach_data['primary_arm']} arm toward {hazard['name']} ({distance:.1f}px)",
                            'time_str': get_current_timestamp_str()
                        }
                        self.alerts_history.append(alert_data)
                
                # Store distance data for drawing
                distance_data.append({
                    'baby_center': baby_center,
                    'hazard_center': hazard_center,
                    'distance': distance,
                    'reach_score': reach_score,
                    'color': color,
                    'alert_level': alert_level,
                    'hazard_box': hazard_box,
                    'is_reaching': reach_data['is_reaching'] if reach_data else False,
                    'reaching_arm': reach_data['primary_arm'] if reach_data else None
                })
        
        # Update alert timing
        if frame_has_critical and current_time - self.last_alert_time > ALERT_COOLDOWN:
            self.last_alert_time = current_time
        
        return distance_data, frame_has_critical
    
    def _build_alert_message(self, alert_type, hazard_name, distance, reach_data):
        """Build alert message including reach information"""
        if reach_data and reach_data['is_reaching']:
            arm = reach_data['primary_arm'].upper()
            reach_pct = reach_data['reach_score']
            return f"{alert_type}: Baby reaching with {arm} arm ({reach_pct:.0f}% extension) toward {hazard_name} ({distance:.1f}px)"
        return f"{alert_type}: Baby near {hazard_name} ({distance:.1f}px)"
    
    def get_recent_alerts(self, seconds=60, limit=10):
        """Get alerts from the last N seconds"""
        current_time = time.time()
        recent = [a for a in self.alerts_history if current_time - a['timestamp'] < seconds]
        return recent[-limit:]
    
    def get_alerts_summary(self):
        """Get alerts summary"""
        return {
            'alerts': self.get_recent_alerts(),
            'total': len(self.get_recent_alerts()),
            'critical_now': len(self.current_critical_alerts),
            'timestamp': time.time()
        }
