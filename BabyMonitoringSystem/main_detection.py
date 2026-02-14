import cv2
from models import get_model
from image_preprocessing import correct_perspective, enhance_image
from face_recognition_module import FamilyFaceRecognition
from roi_detector import get_roi

# Initialize models
model = get_model()
face_recog = FamilyFaceRecognition()
# Register family members (update image paths as needed)
face_recog.register_family("Mother", "mother_photo.jpg")
face_recog.register_family("Father", "father_photo.jpg")

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Step 1: Correct perspective for wall-mounted camera
    corrected = correct_perspective(frame, angle=25)

    # Step 2: Enhance image for small/angled faces
    enhanced = enhance_image(corrected)

    # Step 3: Run YOLO detection on enhanced frame
    results = model.detect(enhanced)

    # Step 4: Find baby/person bounding box
    baby_box = None
    for r in results:
        # Adapt this logic based on YOLO output format
        if hasattr(r, 'boxes'):
            for box in r.boxes:
                class_id = int(box.cls[0])
                class_name = model.get_class_name(class_id)
                if class_name == 'baby':
                    x1, y1, x2, y2 = map(int, box.xyxy[0])
                    baby_box = (x1, y1, x2, y2)
                    break

    if baby_box:
        roi = get_roi(enhanced, baby_box)
        faces = face_recog.recognize(roi)
        for name, location in faces:
            print(f"Detected: {name} at {location}")
    else:
        print("No baby detected")

    # Display for debugging
    cv2.imshow("Frame", enhanced)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
