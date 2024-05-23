import os
import face_recognition
import cv2

def load_known_faces(known_faces_dir):
    known_face_encodings = []
    known_face_names = []

    for filename in os.listdir(known_faces_dir):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            img_path = os.path.join(known_faces_dir, filename)
            image = face_recognition.load_image_file(img_path)
            face_encoding = face_recognition.face_encodings(image)[0]
            known_face_encodings.append(face_encoding)
            known_face_names.append(os.path.splitext(filename)[0])
    
    return known_face_encodings, known_face_names

def capture_frame_from_webcam():
    video_capture = cv2.VideoCapture(0)
    ret, frame = video_capture.read()
    video_capture.release()
    return frame

def detect_faces_in_frame(frame):
    rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    return face_locations, face_encodings

def compare_faces(known_face_encodings, face_encodings):
    matches = face_recognition.compare_faces(known_face_encodings, face_encodings)
    return matches

def identify_user(matches, known_face_names):
    for i, match in enumerate(matches):
        if match:
            return known_face_names[i]
    return None
