def get_roi(frame, baby_box, margin=100):
    x1, y1, x2, y2 = baby_box
    h, w = frame.shape[:2]
    roi = frame[max(0, y1-margin):min(h, y2+margin), max(0, x1-margin):min(w, x2+margin)]
    return roi
