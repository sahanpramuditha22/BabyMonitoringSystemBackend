"""
Configuration settings for the Baby Safety Monitoring System
"""

# Model configuration
MODEL_PATH = 'my_model4.pt'
CONFIDENCE_THRESHOLD = 0.5

# Distance thresholds (in pixels)
CRITICAL_DISTANCE = 100
WARNING_DISTANCE = 200

# Alert settings
ALERT_COOLDOWN = 5  # seconds between alert sounds
ALERT_HISTORY_LIMIT = 60  # seconds to keep alerts
RECENT_ALERTS_LIMIT = 10  # number of recent alerts to return

# Camera settings
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
FRAME_DELAY = 0.1  # seconds

# Server settings
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 5001
DEBUG_MODE = False
THREADED = True
