import cv2
import pygame
import subprocess
from pythonosc import dispatcher as osc_dispatcher, osc_server
import os

# Initialize Pygame
pygame.mixer.init()

# Load animal images (3D models)
animal_images = {
    0: 'animated_triceratops_skeleton.glb',   # Add triceratops skeleton image
    1: 'tyrannosaurus_rex_skeleton.glb',      # Add T-Rex skeleton image
    2: 'utahraptor_skeleton.glb'              # Add Utahraptor skeleton image
    # Add more mappings as needed
}

# Load animal sounds
animal_sounds = {
    0: 'triceratops.mp3',  
    1: 't-rex.mp3', 
    2: 'tahraptor.mp3'
    # Add more mappings as needed
}

# Animal info text
animal_info = {
    0: "Triceratops: A herbivorous dinosaur known for its large bony frill and three horns on its face.",
    1: "Tyrannosaurus Rex: One of the largest land carnivores of all time, known for its massive jaws and powerful legs.",
    2: "Utahraptor: A genus of theropod dinosaur, known for its large sickle-shaped claw on each hindfoot."
}

# Path to 3D Viewer executable
three_d_viewer_path = r"C:\Program Files\WindowsApps\Microsoft.Microsoft3DViewer_10.2103.13010.0_x64__8wekyb3d8bbwe\3DViewer.exe"

# Dictionary to keep track of opened images and text files
opened_files = {}

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
                    info_text = animal_info.get(marker_id, "")
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

# Function to handle TUIO messages
def tuio_handler(address, *args):
    try:
        # Ensure that args has enough elements for extracting TUIO message parameters
        if len(args) >= 3:
            # Extract TUIO message parameters
            marker_id = abs(int(args[2]))  # Convert to absolute value and integer
            print("Received TUIO message:", args)  # Print entire TUIO message for debugging
            print("Marker ID:", marker_id)

            # Display model and text if it hasn't been opened yet
            if marker_id not in opened_files:
                display_model_and_text(marker_id)

            # Play sound
            play_sound(marker_id)
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
