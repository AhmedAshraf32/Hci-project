import tkinter as tk
import subprocess
import pygame
import cv2
import mediapipe as mp
import threading
from dollarpy import Recognizer, Template, Point


# Initialize Pygame
pygame.mixer.init()

# Load animal images (3D models)
animal_images = [
    'animated_triceratops_skeleton.glb',  # Add triceratops skeleton image
    'tyrannosaurus_rex_skeleton.glb',     # Add T-Rex skeleton image
    'utahraptor_skeleton.glb'             # Add Utahraptor skeleton image
]

# Load animal sounds
animal_sounds = [
    'triceratops.mp3',
    't-rex.mp3',
    'tahraptor.mp3'
]

# Animal info text
animal_info = [
    "Triceratops: A herbivorous dinosaur known for its large bony frill and three horns on its face.",
    "Tyrannosaurus Rex: One of the largest land carnivores of all time, known for its massive jaws and powerful legs.",
    "Utahraptor: A genus of theropod dinosaur, known for its large sickle-shaped claw on each hindfoot."
]

# Path to 3D Viewer executable
three_d_viewer_path = r"C:\Program Files\WindowsApps\Microsoft.Microsoft3DViewer_10.2103.13010.0_x64__8wekyb3d8bbwe\3DViewer.exe"

# Global variable to track the current model index
current_model_index = 0

# Function to display model using 3D Viewer
def display_model(index):
    try:
        model_file = animal_images[index]
        subprocess.run(['start', three_d_viewer_path, model_file], shell=True)
    except Exception as e:
        print("Error displaying model:", e)

# Function to play sound using Pygame
def play_sound(index):
    try:
        sound_file = animal_sounds[index]
        sound = pygame.mixer.Sound(sound_file)
        sound.play()
    except Exception as e:
        print("Error playing sound:", e)

# Function to display information text
def display_info(index):
    info_text = animal_info[index]
    info_label.config(text=info_text)

# Function to switch models
def switch_model(index):
    display_model(index)
    play_sound(index)
    display_info(index)

# Function to switch to the next model
def next_model():
    global current_model_index
    current_model_index = (current_model_index + 1) % len(animal_images)
    switch_model(current_model_index)

# Function to switch to the previous model
def previous_model():
    global current_model_index
    current_model_index = (current_model_index - 1) % len(animal_images)
    switch_model(current_model_index)


# initialize Pose estimator
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

pose = mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

cap = cv2.VideoCapture(0)
framecnt=0

SwipeLeftLH = Template('SwipeLeftLH', [
Point(183,317, 1),
Point(308,309, 1),
Point(183,317, 1),
Point(308,309, 1),
Point(183,317, 1),
Point(308,309, 1),
Point(183,317, 1),
Point(309,310, 1),
Point(183,317, 1),
Point(309,310, 1),
Point(183,317, 1),
Point(309,310, 1),
Point(183,317, 1),
Point(309,311, 1),
Point(183,316, 1),
Point(308,307, 1),
Point(183,315, 1),
Point(306,298, 1),
Point(183,315, 1),
Point(304,287, 1),
Point(183,316, 1),
Point(300,264, 1),
Point(186,317, 1),
Point(293,249, 1),
Point(188,319, 1),
Point(286,237, 1),
Point(190,319, 1),
Point(279,228, 1),
Point(191,318, 1),
Point(270,222, 1),
Point(191,318, 1),
Point(262,216, 1),
Point(190,317, 1),
Point(254,210, 1),
Point(189,317, 1),
Point(250,205, 1),
Point(189,316, 1),
Point(249,203, 1),
Point(189,316, 1),
Point(251,200, 1),
Point(189,315, 1),
Point(255,199, 1),
Point(189,314, 1),
Point(263,195, 1),
Point(190,313, 1),
Point(279,194, 1),
Point(190,313, 1),
Point(294,193, 1),
Point(190,313, 1),
Point(300,187, 1),
Point(190,313, 1),
Point(306,189, 1),
Point(190,312, 1),
Point(307,192, 1),
Point(190,312, 1),
Point(306,193, 1),
Point(189,312, 1),
Point(310,236, 1),
Point(189,312, 1),
Point(308,224, 1),
Point(188,312, 1),
Point(307,211, 1),
Point(188,312, 1),
Point(310,295, 1),
Point(187,312, 1),
Point(311,303, 1),
Point(187,313, 1),
Point(310,304, 1),
Point(185,314, 1),
Point(311,308, 1),
Point(184,314, 1),
Point(312,308, 1),
Point(183,315, 1),
Point(312,308, 1),
Point(182,315, 1),
Point(313,306, 1),
Point(183,315, 1),
Point(313,307, 1),
Point(183,316, 1),
Point(312,307, 1),
Point(183,316, 1),
Point(312,307, 1),
Point(183,316, 1),
Point(312,307, 1),
Point(184,316, 1),
Point(311,307, 1),
Point(185,316, 1),
Point(311,309, 1),
Point(185,316, 1),
Point(310,307, 1),
Point(185,316, 1),
Point(310,308, 1),
Point(186,316, 1),
Point(309,307, 1),
Point(186,316, 1),
Point(309,307, 1),
Point(186,316, 1),
Point(309,307, 1),
Point(186,316, 1),
Point(310,308, 1),
Point(186,316, 1),
Point(310,309, 1),
Point(186,317, 1),
Point(310,309, 1),
Point(186,318, 1),
Point(310,311, 1),
Point(186,321, 1),
Point(310,312, 1),
Point(186,320, 1),
Point(311,313, 1),
Point(185,322, 1),
Point(311,313, 1),
Point(184,322, 1),
Point(311,313, 1),
Point(183,324, 1),
Point(311,314, 1),
Point(183,325, 1),
Point(311,315, 1),
Point(183,324, 1),
Point(311,315, 1),
Point(183,324, 1),
Point(311,315, 1),
Point(183,324, 1),
Point(311,315, 1),
Point(184,324, 1),
Point(311,315, 1),
Point(186,324, 1),
Point(311,315, 1),
Point(187,324, 1),
Point(311,315, 1),
Point(188,324, 1),
Point(311,314, 1),
Point(188,324, 1),
Point(311,314, 1),
Point(189,324, 1),
Point(311,314, 1),
Point(190,323, 1),
Point(311,313, 1),
Point(192,323, 1),
Point(311,313, 1),
Point(194,324, 1),
Point(311,313, 1),
Point(195,324, 1),
Point(311,312, 1),
Point(196,324, 1),
Point(311,311, 1),
])
SwipeLeftRH = Template('SwipeLeftRH', [
Point(178,323, 1),
Point(310,314, 1),
Point(175,326, 1),
Point(310,316, 1),
Point(175,327, 1),
Point(310,318, 1),
Point(177,327, 1),
Point(310,318, 1),
Point(178,324, 1),
Point(310,319, 1),
Point(178,323, 1),
Point(310,320, 1),
Point(178,322, 1),
Point(310,321, 1),
Point(178,322, 1),
Point(310,321, 1),
Point(178,322, 1),
Point(310,321, 1),
Point(179,322, 1),
Point(310,320, 1),
Point(180,322, 1),
Point(311,320, 1),
Point(181,321, 1),
Point(310,321, 1),
Point(183,321, 1),
Point(310,321, 1),
Point(183,321, 1),
Point(310,321, 1),
Point(184,321, 1),
Point(310,320, 1),
Point(184,321, 1),
Point(311,319, 1),
Point(184,320, 1),
Point(311,317, 1),
Point(186,318, 1),
Point(311,317, 1),
Point(186,306, 1),
Point(311,315, 1),
Point(188,293, 1),
Point(311,316, 1),
Point(188,288, 1),
Point(310,316, 1),
Point(188,276, 1),
Point(309,316, 1),
Point(188,265, 1),
Point(309,316, 1),
Point(188,255, 1),
Point(309,315, 1),
Point(188,245, 1),
Point(309,311, 1),
Point(188,240, 1),
Point(309,311, 1),
Point(188,232, 1),
Point(309,313, 1),
Point(187,226, 1),
Point(309,317, 1),
Point(188,223, 1),
Point(310,320, 1),
Point(190,222, 1),
Point(311,323, 1),
Point(198,216, 1),
Point(311,322, 1),
Point(208,215, 1),
Point(311,322, 1),
Point(218,214, 1),
Point(310,322, 1),
Point(226,217, 1),
Point(310,319, 1),
Point(234,216, 1),
Point(309,319, 1),
Point(239,219, 1),
Point(308,322, 1),
Point(245,220, 1),
Point(309,334, 1),
Point(251,221, 1),
Point(309,338, 1),
Point(255,221, 1),
Point(313,336, 1),
Point(258,222, 1),
Point(313,334, 1),
Point(260,224, 1),
Point(312,329, 1),
Point(265,224, 1),
Point(311,307, 1),
Point(266,226, 1),
Point(309,307, 1),
Point(267,233, 1),
Point(301,259, 1),
Point(263,253, 1),
Point(291,246, 1),
Point(262,268, 1),
Point(293,266, 1),
Point(261,291, 1),
Point(292,281, 1),
Point(244,308, 1),
Point(286,307, 1),
Point(231,321, 1),
Point(289,320, 1),
Point(223,324, 1),
Point(290,326, 1),
Point(222,328, 1),
Point(288,328, 1),
Point(221,335, 1),
Point(284,330, 1),
Point(218,334, 1),
Point(285,333, 1),
Point(216,338, 1),
Point(286,334, 1),
Point(213,334, 1),
Point(286,333, 1),
Point(201,333, 1),
Point(287,334, 1),
Point(207,332, 1),
Point(287,332, 1),
Point(203,333, 1),
Point(287,330, 1),
Point(204,334, 1),
Point(287,330, 1),
Point(204,332, 1),
Point(286,326, 1),
Point(0, 0, 1),
Point(0, 0, 1),
])
SwipeRightLH = Template('SwipeRightLH', [
Point(193,330, 1),
Point(309,311, 1),
Point(192,326, 1),
Point(309,312, 1),
Point(192,325, 1),
Point(309,312, 1),
Point(192,324, 1),
Point(309,311, 1),
Point(192,324, 1),
Point(309,311, 1),
Point(192,324, 1),
Point(309,311, 1),
Point(193,323, 1),
Point(309,311, 1),
Point(193,323, 1),
Point(309,311, 1),
Point(193,323, 1),
Point(309,311, 1),
Point(193,323, 1),
Point(310,311, 1),
Point(193,323, 1),
Point(310,311, 1),
Point(193,323, 1),
Point(310,311, 1),
Point(193,323, 1),
Point(310,311, 1),
Point(192,323, 1),
Point(310,311, 1),
Point(192,323, 1),
Point(311,311, 1),
Point(192,323, 1),
Point(311,311, 1),
Point(192,323, 1),
Point(311,311, 1),
Point(191,322, 1),
Point(311,310, 1),
Point(191,322, 1),
Point(311,310, 1),
Point(191,321, 1),
Point(311,310, 1),
Point(191,321, 1),
Point(311,310, 1),
Point(191,321, 1),
Point(311,311, 1),
Point(191,321, 1),
Point(311,311, 1),
Point(190,321, 1),
Point(311,312, 1),
Point(190,321, 1),
Point(311,312, 1),
Point(190,321, 1),
Point(311,312, 1),
Point(189,322, 1),
Point(310,313, 1),
Point(189,322, 1),
Point(310,313, 1),
Point(189,322, 1),
Point(310,313, 1),
Point(189,322, 1),
Point(310,313, 1),
Point(189,321, 1),
Point(310,313, 1),
Point(189,321, 1),
Point(310,310, 1),
Point(189,321, 1),
Point(308,307, 1),
Point(189,321, 1),
Point(308,302, 1),
Point(189,321, 1),
Point(308,300, 1),
Point(188,320, 1),
Point(309,265, 1),
Point(188,320, 1),
Point(309,235, 1),
Point(187,319, 1),
Point(308,223, 1),
Point(187,319, 1),
Point(306,211, 1),
Point(188,319, 1),
Point(304,209, 1),
Point(188,319, 1),
Point(301,207, 1),
Point(187,320, 1),
Point(301,195, 1),
Point(187,321, 1),
Point(302,196, 1),
Point(187,321, 1),
Point(301,192, 1),
Point(187,319, 1),
Point(291,188, 1),
Point(188,318, 1),
Point(280,186, 1),
Point(189,318, 1),
Point(270,188, 1),
Point(188,318, 1),
Point(253,188, 1),
Point(188,334, 1),
Point(239,190, 1),
Point(187,331, 1),
Point(231,193, 1),
Point(186,330, 1),
Point(229,202, 1),
Point(186,329, 1),
Point(226,208, 1),
Point(185,328, 1),
Point(226,211, 1),
Point(185,328, 1),
Point(225,212, 1),
Point(185,329, 1),
Point(225,212, 1),
Point(185,329, 1),
Point(226,212, 1),
Point(186,333, 1),
Point(229,212, 1),
Point(185,333, 1),
Point(230,212, 1),
Point(185,335, 1),
Point(231,215, 1),
Point(184,334, 1),
Point(232,220, 1),
Point(193,322, 1),
Point(232,225, 1),
Point(205,247, 1),
Point(239,239, 1),
Point(214,248, 1),
Point(254,259, 1),
Point(213,313, 1),
Point(262,283, 1),
Point(199,323, 1),
Point(275,309, 1),
Point(192,322, 1),
Point(293,317, 1),
Point(189,322, 1),
Point(300,324, 1),
Point(189,320, 1),
Point(306,319, 1),
Point(188,320, 1),
Point(308,320, 1),
Point(188,320, 1),
Point(309,318, 1),
Point(188,319, 1),
Point(310,315, 1),
Point(188,320, 1),
Point(312,314, 1),
Point(187,320, 1),
Point(313,317, 1),
Point(186,320, 1),
Point(313,317, 1),
Point(186,320, 1),
Point(312,318, 1),
Point(185,320, 1),
Point(311,317, 1),
Point(185,320, 1),
Point(311,317, 1),
Point(184,320, 1),
Point(311,317, 1),
Point(184,319, 1),
Point(311,317, 1),
Point(184,319, 1),
Point(311,316, 1),
Point(184,319, 1),
Point(310,316, 1),
Point(184,319, 1),
Point(310,316, 1),
Point(184,318, 1),
Point(310,316, 1),
Point(184,318, 1),
Point(310,316, 1),
Point(185,319, 1),
Point(310,318, 1),
Point(185,320, 1),
Point(309,318, 1),
Point(185,321, 1),
Point(309,318, 1),
Point(185,321, 1),
Point(308,318, 1),
Point(185,321, 1),
Point(308,318, 1),
Point(186,321, 1),
Point(308,318, 1),
Point(186,321, 1),
Point(309,318, 1),
Point(187,321, 1),
Point(309,318, 1),
Point(187,320, 1),
Point(308,317, 1),
Point(188,320, 1),
Point(309,316, 1),
Point(188,320, 1),
Point(309,315, 1),
Point(188,320, 1),
Point(309,315, 1),
Point(189,319, 1),
Point(309,314, 1),
])
SwipeRightRH = Template('SwipeRightRH', [
Point(189,322, 1),
Point(309,312, 1),
Point(189,322, 1),
Point(310,311, 1),
Point(189,322, 1),
Point(310,311, 1),
Point(189,322, 1),
Point(310,312, 1),
Point(190,322, 1),
Point(310,312, 1),
Point(193,322, 1),
Point(311,312, 1),
Point(197,319, 1),
Point(311,313, 1),
Point(201,314, 1),
Point(311,313, 1),
Point(206,307, 1),
Point(311,313, 1),
Point(210,290, 1),
Point(311,313, 1),
Point(214,281, 1),
Point(311,313, 1),
Point(217,271, 1),
Point(310,314, 1),
Point(219,261, 1),
Point(310,314, 1),
Point(221,254, 1),
Point(310,316, 1),
Point(222,248, 1),
Point(310,317, 1),
Point(224,243, 1),
Point(310,318, 1),
Point(223,240, 1),
Point(309,318, 1),
Point(224,236, 1),
Point(309,318, 1),
Point(223,233, 1),
Point(309,318, 1),
Point(222,230, 1),
Point(309,316, 1),
Point(218,228, 1),
Point(308,312, 1),
Point(213,227, 1),
Point(308,313, 1),
Point(206,223, 1),
Point(308,313, 1),
Point(198,223, 1),
Point(308,314, 1),
Point(191,221, 1),
Point(309,314, 1),
Point(184,219, 1),
Point(308,314, 1),
Point(182,217, 1),
Point(308,312, 1),
Point(180,217, 1),
Point(307,310, 1),
Point(178,216, 1),
Point(307,309, 1),
Point(178,218, 1),
Point(307,309, 1),
Point(178,219, 1),
Point(307,309, 1),
Point(179,219, 1),
Point(306,310, 1),
Point(180,220, 1),
Point(307,313, 1),
Point(180,225, 1),
Point(307,314, 1),
Point(181,243, 1),
Point(307,314, 1),
Point(181,267, 1),
Point(308,314, 1),
Point(180,259, 1),
Point(308,313, 1),
Point(178,288, 1),
Point(309,313, 1),
Point(177,313, 1),
Point(310,315, 1),
Point(176,315, 1),
Point(310,315, 1),
Point(176,318, 1),
Point(310,315, 1),
Point(0, 0, 1),
Point(0, 0, 1),
])


recognizer = Recognizer([SwipeLeftLH,SwipeLeftRH,SwipeRightLH,SwipeRightRH])

Allpoints=[]



def camera_capture():
    global framecnt
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        frame = cv2.resize(frame, (480, 320))
        framecnt += 1
        try:
            RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(RGB)
            image_height, image_width, _ = frame.shape
            x = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x * image_width))
            y = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y * image_height))
            Allpoints.append(Point(x, y, 1))
            x = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x * image_width))
            y = (int(results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y * image_height))
            Allpoints.append(Point(x, y, 1))

            if framecnt % 30 == 0:
                framecnt = 0
                result = recognizer.recognize(Allpoints)
                print(result)
                Allpoints.clear()

                if result[0] == "SwipeRightLH" or result[0] == "SwipeRightRH":
                    next_model()
                elif result[0] == "SwipeLeftLH" or result[0] == "SwipeLeftRH":
                    previous_model()

            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
            cv2.imshow('Output', frame)
        except Exception as e:
            print('Camera Error:', e)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Create the main window using Tkinter
root = tk.Tk()
root.title("3D Model Viewer")
root.geometry("600x400")

# Add a label to display animal information
info_label = tk.Label(root, text="", wraplength=500, justify=tk.LEFT)
info_label.pack(pady=20)

# Bind the 'x' key to switch models
root.bind('<x>', switch_model)

# Initial display
display_model(current_model_index)
play_sound(current_model_index)
display_info(current_model_index)

# Start the camera capture in a separate thread
camera_thread = threading.Thread(target=camera_capture)
camera_thread.start()

# Run the Tkinter event loop
root.mainloop()
