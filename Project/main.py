import tkinter as tk
from tkinter import ttk, messagebox
import subprocess

def gesture_action():
    try:
        subprocess.run(["python", "Gestures.py"])
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run glb.py: {e}")

def ar_action():
    messagebox.showinfo("AR", "AR button clicked!")

def tuio_action():
    try:
        subprocess.Popen(['python', 'glb.py'])  # Change 'glb.py' to the correct path if necessary
        messagebox.showinfo("TUIO Markers", "TUIO Markers script started!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start TUIO Markers script: {e}")


# Function to change button color on hover
def on_enter(e):
    e.widget['background'] = '#ffcccb'

def on_leave(e):
    e.widget['background'] = '#ff6666'

# Create the main window
root = tk.Tk()
root.title("Main Window")
root.geometry("400x300")  # Set the size of the window
root.configure(bg='#e6f7ff')  # Set the background color

# Apply a style to the buttons
style = ttk.Style()
style.configure('TButton', font=('Helvetica', 12, 'bold'), padding=10, background='#ff6666', foreground='white')
style.map('TButton', foreground=[('active', '#ffffff')], background=[('active', '#ff3333')])

# Create a frame for the buttons
frame = tk.Frame(root, bg='#e6f7ff', bd=5)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

# Create buttons
gesture_button = tk.Button(frame, text="Gesture", command=gesture_action, font=('Helvetica', 12, 'bold'), bg='#ff6666', fg='white', activebackground='#ff3333', activeforeground='white')
ar_button = tk.Button(frame, text="AR", command=ar_action, font=('Helvetica', 12, 'bold'), bg='#ff6666', fg='white', activebackground='#ff3333', activeforeground='white')
tuio_button = tk.Button(frame, text="TUIO Markers", command=tuio_action, font=('Helvetica', 12, 'bold'), bg='#ff6666', fg='white', activebackground='#ff3333', activeforeground='white')

# Place buttons in the frame with padding
gesture_button.pack(pady=10, fill=tk.X)
ar_button.pack(pady=10, fill=tk.X)
tuio_button.pack(pady=10, fill=tk.X)

# Bind hover effects to buttons
gesture_button.bind("<Enter>", on_enter)
gesture_button.bind("<Leave>", on_leave)
ar_button.bind("<Enter>", on_enter)
ar_button.bind("<Leave>", on_leave)
tuio_button.bind("<Enter>", on_enter)
tuio_button.bind("<Leave>", on_leave)

# Run the application
root.mainloop()
