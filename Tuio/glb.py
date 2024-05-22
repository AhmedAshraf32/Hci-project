import cv2
import pygame
import subprocess
from pythonosc import dispatcher as osc_dispatcher, osc_server
import os
import pyautogui
import time

# Initialize Pygame
pygame.mixer.init()

# Load animal images (3D models)
animal_images = {
    0: 'animated_triceratops_skeleton.glb',
    1: 'tyrannosaurus_rex_skeleton.glb',
    2: 'utahraptor_skeleton.glb'
    # Add more mappings as needed
}

# Load animal sounds
animal_sounds = {
    0: 'triceratops.mp3',
    1: 't-rex.mp3',
    2: 'utahraptor.mp3'
    # Add more mappings as needed
}

# Function to read animal info from text files
def load_animal_info(marker_id):
    info_file = f"info_{marker_id}.txt"
    try:
        with open(info_file, "r") as f:
            return f.read()
    except FileNotFoundError:
        return "Information file not found."
    except Exception as e:
        return f"Error reading information file: {e}"

# Path to 3D Viewer executable
three_d_viewer_path = r"C:\Program Files\WindowsApps\Microsoft.Microsoft3DViewer_10.2103.13010.0_x64__8wekyb3d8bbwe\3DViewer.exe"

# Dictionary to keep track of opened images and text files
opened_files = {}
previous_rotation = {}

# Function to display model using 3D Viewer and open a text file with info
def display_model_and_text(marker_id):
    try:
        # Ensure that the marker ID exists in animal_images dictionary
        if marker_id in animal_images:
            # Display 3D model
            model_file = animal_images.get(marker_id)
            if model_file:
                # Open the model with 3D Viewer
                subprocess.run(['start', three_d_viewer_path, model_file], shell=True)

                # Create and open a text file with the info (if not already opened)
                if marker_id not in opened_files:
                    info_text = load_animal_info(marker_id)
                    info_file = f"info_{marker_id}.txt"
                    with open(info_file, "w") as f:
                        f.write(info_text)
                    # Open the text file with the default text editor
                    os.startfile(info_file)
                    opened_files[marker_id] = info_file  # Mark the text file as opened
            else:
                print("Model not found for marker ID:", marker_id)
        else:
            print("Marker ID:", marker_id, "not found in model dictionary")
    except Exception as e:
        print("Error:", e)
        # Function to play sound using Pygame
def play_sound(marker_id):
    try:
        # Ensure that the marker ID exists in animal_sounds dictionary
        if marker_id in animal_sounds:
            # Play sound
            sound_file = animal_sounds.get(marker_id)
            if sound_file:
                sound = pygame.mixer.Sound(sound_file)
                sound.play()
            else:
                print("Sound not found for marker ID:", marker_id)
        else:
            print("Marker ID:", marker_id, "not found in sound dictionary")
    except Exception as e:
        print("Error:", e)

# Function to focus on Notepad window
def focus_notepad():
    try:
        notepad = pyautogui.getWindowsWithTitle("Notepad")
        if notepad:
            notepad[0].activate()
            print("Focused on Notepad.")
        else:
            print("Notepad is not open.")
    except Exception as e:
        print("Error focusing on Notepad:", e)

# Function to handle TUIO messages
def tuio_handler(address, *args):
    try:
        if len(args) >= 4:
            marker_id = abs(int(args[2]))  # Convert to absolute value and integer
            rotation_angle = args[3]      # Extract rotation angle
            print("Received TUIO message:", args)  # Print entire TUIO message for debugging
            print("Marker ID:", marker_id)
            print("Rotation Angle:", rotation_angle)

            # Display model and text if it hasn't been opened yet
            if marker_id not in opened_files:
                display_model_and_text(marker_id)

            # Play sound
            play_sound(marker_id)

            # Initialize previous rotation angle if not set
            if marker_id not in previous_rotation:
                previous_rotation[marker_id] = rotation_angle

            # Simulate scroll down in Notepad when marker rotates
            rotation_threshold = 0.02  # Reduce the threshold for rotation changes
            rotation_change = abs(rotation_angle - previous_rotation[marker_id])
            print(f"Rotation change detected: {rotation_change}")

            if rotation_change > rotation_threshold:
                print(f"Scrolling due to rotation change. Previous: {previous_rotation[marker_id]}, Current: {rotation_angle}")
                focus_notepad()  # Focus on Notepad before scrolling
                time.sleep(0.5)  # Small delay to ensure focus
                pyautogui.scroll(-10)  # Scroll down
                print("Scrolled down.")
                previous_rotation[marker_id] = rotation_angle
            else:
                print(f"No significant rotation change. Previous: {previous_rotation[marker_id]}, Current: {rotation_angle}")

        else:
            print("Insufficient parameters in TUIO message:", args)
    except Exception as e:
        print("Error processing TUIO message:", e)

# Create a dispatcher to route OSC messages
osc_dispatcher = osc_dispatcher.Dispatcher()
osc_dispatcher.map("/tuio/2Dobj", tuio_handler)  # Map TUIO object messages to handler function

# Create an OSC server to listen for TUIO messages
server = osc_server.ThreadingOSCUDPServer(("localhost", 3333), osc_dispatcher)

# Start the OSC server
print("Listening for TUIO messages on port 3333...")
server.serve_forever()
