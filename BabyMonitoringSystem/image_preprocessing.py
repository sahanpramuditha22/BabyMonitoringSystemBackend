import cv2
import numpy as np

def correct_perspective(frame, angle=25):
    """Compensate for top-down camera angle"""
    height, width = frame.shape[:2]
    pts1 = np.float32([[0,0], [width,0], [0,height], [width,height]])
    pts2 = np.float32([
        [0 + angle*2, 0],
        [width - angle*2, 0],
        [0, height],
        [width, height]
    ])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    return cv2.warpPerspective(frame, matrix, (width, height))

def enhance_image(frame):
    """Sharpen and boost contrast for small faces"""
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sharpened = cv2.filter2D(frame, -1, kernel)
    lab = cv2.cvtColor(sharpened, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8))
    l = clahe.apply(l)
    enhanced_lab = cv2.merge((l, a, b))
    return cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
