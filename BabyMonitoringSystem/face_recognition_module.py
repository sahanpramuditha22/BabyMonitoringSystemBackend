import face_recognition
import cv2

class FamilyFaceRecognition:
    def __init__(self):
        self.known_encodings = []
        self.known_names = []

    def register_family(self, name, image_path):
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        self.known_encodings.append(encoding)
        self.known_names.append(name)

    def recognize(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(
            rgb_frame, number_of_times_to_upsample=2, model="cnn"
        )
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
        results = []
        for encoding, location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(self.known_encodings, encoding)
            name = "Stranger"
            if True in matches:
                name = self.known_names[matches.index(True)]
            results.append((name, location))
        return results
