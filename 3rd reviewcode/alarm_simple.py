import tkinter as tk
from tkinter import messagebox
import time
import threading
import pyttsx3

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def check_alarm():
    """Check if the current time matches the alarm time."""
    alarm_time = user_input.get()
    
    if alarm_time == "":
        messagebox.showwarning("Error", "Please enter a time (HH:MM)")
        return
    
    # Validate time format
    try:
        hours, minutes = map(int, alarm_time.split(':'))
        if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Error", "Invalid time format. Use HH:MM (24-hour format)")
        return
    
    # Update status
    status_label.config(text=f"Alarm set for {alarm_time}")
    speak(f"Alarm set for {alarm_time}")
    
    # Start alarm thread
    alarm_thread = threading.Thread(target=wait_for_alarm, args=(alarm_time,))
    alarm_thread.daemon = True
    alarm_thread.start()

def wait_for_alarm(alarm_time):
    """Wait until the alarm time is reached."""
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == alarm_time:
            trigger_alarm()
            break
        time.sleep(1)
        
        # Update current time display
        current_time_label.config(text=f"Current time: {time.strftime('%H:%M:%S')}")

def trigger_alarm():
    """Actions to take when alarm time is reached."""
    messagebox.showinfo("Alarm", "Time's up!")
    speak("Time's up! Your alarm is ringing.")
    status_label.config(text="Alarm triggered!")

# Create main window
root = tk.Tk()
root.title("Simple Alarm Clock")
root.geometry("400x300")
root.configure(bg="#f0f0f0")

# Create a frame for better organization
main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# Header
header_label = tk.Label(main_frame, text="Alarm Clock", font=("Arial", 18, "bold"), bg="#f0f0f0")
header_label.pack(pady=(0, 20))

# Current time display
current_time_label = tk.Label(main_frame, text=f"Current time: {time.strftime('%H:%M:%S')}", 
                             font=("Arial", 12), bg="#f0f0f0")
current_time_label.pack(pady=(0, 20))

# Update current time every second
def update_time():
    current_time_label.config(text=f"Current time: {time.strftime('%H:%M:%S')}")
    root.after(1000, update_time)
root.after(1000, update_time)

# Input frame
input_frame = tk.Frame(main_frame, bg="#f0f0f0")
input_frame.pack(pady=10)

# Time input label
input_label = tk.Label(input_frame, text="Set alarm time (HH:MM):", font=("Arial", 12), bg="#f0f0f0")
input_label.pack(side=tk.LEFT, padx=(0, 10))

# Time input field
user_input = tk.Entry(input_frame, font=("Arial", 12), width=8)
user_input.pack(side=tk.LEFT)

# Set alarm button
set_button = tk.Button(main_frame, text="Set Alarm", font=("Arial", 12, "bold"),
                      bg="#4CAF50", fg="white", padx=10, pady=5, command=check_alarm)
set_button.pack(pady=20)

# Status label
status_label = tk.Label(main_frame, text="No alarm set", font=("Arial", 12), bg="#f0f0f0")
status_label.pack()

# Initial message
speak("Welcome to the Alarm Clock. Please enter a time in 24-hour format.")

# Start the GUI
root.mainloop()