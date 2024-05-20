import cv2
from utils import load_known_faces, capture_frame_from_webcam, detect_faces_in_frame, compare_faces, identify_user

def main():
    known_faces_dir = 'known_faces'
    known_face_encodings, known_face_names = load_known_faces(known_faces_dir)

    print("Press 'q' to quit.")
    while True:
        frame = capture_frame_from_webcam()
        face_locations, face_encodings = detect_faces_in_frame(frame)

        if face_encodings:
            matches = compare_faces(known_face_encodings, face_encodings)
            user = identify_user(matches, known_face_names)

            if user:
                print(f"User identified: {user}")
            else:
                print("No match found.")

        # Display the frame with detected faces
        for (top, right, bottom, left) in face_locations:
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        cv2.imshow('Video', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
