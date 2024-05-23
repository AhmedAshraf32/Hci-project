import cv2
import dlib
import numpy as np
import os
from utils import load_known_faces_and_encodings

# Load the models
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_rec_model = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# Load known faces
known_face_encodings, known_face_names = load_known_faces_and_encodings("known_faces")

def recognize_faces_in_frame(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    faces = detector(rgb_frame, 1)  # Detect faces

    names = []
    for face in faces:
        shape = predictor(rgb_frame, face)  # Get landmarks
        face_descriptor = np.array(face_rec_model.compute_face_descriptor(rgb_frame, shape))  # Get descriptor

        # Compare face descriptor with known faces
        distances = np.linalg.norm(known_face_encodings - face_descriptor, axis=1)
        best_match_index = np.argmin(distances)
        if distances[best_match_index] < 0.6:  # Threshold for recognition
            name = known_face_names[best_match_index]
            names.append(name)
        else:
            names.append(None)

        # Draw rectangle and name
        cv2.rectangle(frame, (face.left(), face.top()), (face.right(), face.bottom()), (0, 255, 0), 2)
        if names[-1]:
            cv2.putText(frame, names[-1], (face.left(), face.top() - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    return frame, names

def main():
    video_capture = cv2.VideoCapture(0)  # Start webcam

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        frame, names = recognize_faces_in_frame(frame)
        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
