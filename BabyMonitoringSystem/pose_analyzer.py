"""
Pose analysis for detecting baby reaching behavior
"""
import cv2
import mediapipe as mp
import math
from config import FRAME_WIDTH, FRAME_HEIGHT


class PoseAnalyzer:
    """Analyzes baby posture and reaching behavior"""
    
    def __init__(self):
        """Initialize MediaPipe Pose"""
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.mp_drawing = mp.solutions.drawing_utils
    
    def analyze_reach_posture(self, frame):
        """
        Analyze frame for reaching posture
        
        Args:
            frame: Video frame
        
        Returns:
            tuple: (pose_landmarks, reach_data)
        """
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(frame_rgb)
        
        reach_data = {
            'is_reaching': False,
            'reach_score': 0,
            'arm_extension': 0,
            'body_lean': 0,
            'primary_arm': None,  # 'left' or 'right'
            'hand_position': None,
            'landmarks': None
        }
        
        if results.pose_landmarks:
            reach_data['landmarks'] = results.pose_landmarks
            reach_data.update(self._calculate_reach_metrics(results.pose_landmarks))
        
        return results, reach_data
    
    def _calculate_reach_metrics(self, landmarks):
        """
        Calculate reach-related metrics from pose landmarks
        
        Returns:
            dict: Reach metrics and scores
        """
        # Key landmark indices
        NOSE = 0
        LEFT_SHOULDER = 11
        RIGHT_SHOULDER = 12
        LEFT_ELBOW = 13
        RIGHT_ELBOW = 14
        LEFT_WRIST = 15
        RIGHT_WRIST = 16
        LEFT_HIP = 23
        RIGHT_HIP = 24
        
        metrics = {
            'is_reaching': False,
            'reach_score': 0,
            'arm_extension': 0,
            'body_lean': 0,
            'primary_arm': None,
            'hand_position': None
        }
        
        try:
            # Get coordinates
            left_wrist = landmarks.landmark[LEFT_WRIST]
            right_wrist = landmarks.landmark[RIGHT_WRIST]
            left_elbow = landmarks.landmark[LEFT_ELBOW]
            right_elbow = landmarks.landmark[RIGHT_ELBOW]
            left_shoulder = landmarks.landmark[LEFT_SHOULDER]
            right_shoulder = landmarks.landmark[RIGHT_SHOULDER]
            nose = landmarks.landmark[NOSE]
            left_hip = landmarks.landmark[LEFT_HIP]
            right_hip = landmarks.landmark[RIGHT_HIP]
            
            # Calculate arm extensions (distance from shoulder to wrist)
            left_arm_length = self._distance_3d(left_shoulder, left_wrist)
            right_arm_length = self._distance_3d(right_shoulder, right_wrist)
            
            # Calculate elbow-wrist distance (arm straightness)
            left_extension = self._distance_3d(left_elbow, left_wrist)
            right_extension = self._distance_3d(right_elbow, right_wrist)
            
            # Determine which arm is reaching more
            left_reach_score = left_extension / (left_arm_length + 0.001) * 100
            right_reach_score = right_extension / (right_arm_length + 0.001) * 100
            
            # Calculate body lean (distance from center to hand)
            body_center_x = (left_hip.x + right_hip.x) / 2
            body_center_y = (left_hip.y + right_hip.y) / 2
            
            left_lean = self._distance_2d(
                (left_wrist.x, left_wrist.y),
                (body_center_x, body_center_y)
            )
            right_lean = self._distance_2d(
                (right_wrist.x, right_wrist.y),
                (body_center_x, body_center_y)
            )
            
            # Determine primary reaching arm
            if left_reach_score > right_reach_score:
                primary_arm = 'left'
                reach_score = left_reach_score
                hand_pos = (int(left_wrist.x * FRAME_WIDTH), int(left_wrist.y * FRAME_HEIGHT))
                body_lean = left_lean
            else:
                primary_arm = 'right'
                reach_score = right_reach_score
                hand_pos = (int(right_wrist.x * FRAME_WIDTH), int(right_wrist.y * FRAME_HEIGHT))
                body_lean = right_lean
            
            # Threshold for reaching (arm extension > 75%)
            is_reaching = reach_score > 75
            
            metrics.update({
                'is_reaching': is_reaching,
                'reach_score': min(reach_score, 100),
                'arm_extension': reach_score,
                'body_lean': body_lean * 100,  # Normalize to percentage
                'primary_arm': primary_arm,
                'hand_position': hand_pos
            })
        
        except Exception as e:
            print(f"Error calculating reach metrics: {e}")
        
        return metrics
    
    @staticmethod
    def _distance_3d(point1, point2):
        """Calculate 3D distance between two landmarks"""
        return math.sqrt(
            (point1.x - point2.x)**2 +
            (point1.y - point2.y)**2 +
            (point1.z - point2.z)**2
        )
    
    @staticmethod
    def _distance_2d(point1, point2):
        """Calculate 2D distance between two points"""
        return math.sqrt(
            (point1[0] - point2[0])**2 +
            (point1[1] - point2[1])**2
        )
    
    def draw_pose(self, frame, landmarks):
        """Draw pose landmarks on frame"""
        if landmarks:
            self.mp_drawing.draw_landmarks(
                frame,
                landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                self.mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
                self.mp_drawing.DrawingSpec(color=(255, 0, 0), thickness=2)
            )
        return frame
    
    def cleanup(self):
        """Clean up resources"""
        self.pose.close()
