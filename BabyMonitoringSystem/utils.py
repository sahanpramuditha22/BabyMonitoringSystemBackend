"""
Utility functions for distance calculations and helpers
"""
import math
from datetime import datetime


def calculate_distance(box1, box2):
    """
    Calculate Euclidean distance between centers of two bounding boxes
    
    Args:
        box1: First bounding box [x1, y1, x2, y2]
        box2: Second bounding box [x1, y1, x2, y2]
    
    Returns:
        tuple: (distance, box1_center, box2_center)
    """
    x1_center = (box1[0] + box1[2]) / 2
    y1_center = (box1[1] + box1[3]) / 2
    x2_center = (box2[0] + box2[2]) / 2
    y2_center = (box2[1] + box2[3]) / 2
    
    distance = math.sqrt((x2_center - x1_center)**2 + (y2_center - y1_center)**2)
    return distance, (int(x1_center), int(y1_center)), (int(x2_center), int(y2_center))


def get_local_ip():
    """Get the server's local IP address"""
    import socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except:
        return "localhost"


def get_current_timestamp_str():
    """Get current timestamp as formatted string"""
    return datetime.now().strftime("%H:%M:%S")
