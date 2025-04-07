# Import necessary packages
'''
import cv2
import time
import subprocess
import numpy as np
import pyttsx3
import wikipedia
import openai
import webbrowser
import pyjokes
import os
import requests
import ctypes
import pyautogui
import keras
import mediapipe as mp
from keras.models import load_model
from PIL import ImageGrab
import datetime

# Initialize text-to-speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

speak('Hi, I am Telex! You can assist me using hand signs.')

# Initialize MediaPipe Hand Detection
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# Load the gesture recognition model
model_path = r"C:\Users\Amjith\Desktop\virtual_pa\3rd reviewcode\mp_hand_gesture"
model = keras.models.load_model(model_path)

# Load class names (FIXED)
gesture_file = r"C:\Users\Amjith\Desktop\virtual_pa\3rd reviewcode\gesture.names"

try:
    with open(gesture_file, 'r') as f:
        classNames = f.read().split('\n')
except FileNotFoundError:
    print(f"Error: {gesture_file} not found! Please ensure it is in the correct directory.")
    exit(1)  # Exit script if file is missing

print("Loaded gesture classes:", classNames)

# Initialize the webcam
cap = cv2.VideoCapture(0)
frame_counter = 0

while True:
    # Read each frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture video.")
        break

    x, y, c = frame.shape
    frame = cv2.flip(frame, 1)  # Flip the frame
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    className = ''
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])

            # Draw landmarks
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
            frame_counter += 1

            # Predict gesture after 3 seconds (FIXED)
            if frame_counter == 90:
                prediction = model.predict(np.array([landmarks]))  # Convert list to NumPy array
                classID = np.argmax(prediction)
                className = classNames[classID]
            if frame_counter == 91:
                frame_counter = 0
                className = ''

    # Show the prediction on the frame
    cv2.putText(frame, className, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2, cv2.LINE_AA)

    # Execute commands based on gesture
    if 'peace' in className:
        speak('Peace sign detected. Checking temperature.')
        #exec(open("temperature.py").read())
        #exec(open(r"C:\Users\Amjith\Desktop\virtual_pa\3rd reviewcode\temperature.py").read())
        exec(open(r"C:\Users\Amjith\Desktop\virtual_pa\3rd reviewcode\temperature.py", encoding="utf-8").read())


    elif 'thumbs down' in className:
        speak('Thumbs down detected. Activating ChatGPT.')
        exec(open("chatgpt.py").read())

    elif 'live long' in className:
        speak('Live long sign detected. Opening Gmail.')
        webbrowser.open_new_tab("https://www.gmail.com")

    elif 'thumbs up' in className:
        speak('Thumbs up detected. Opening Notepad.')
        subprocess.run([r'C:\Windows\System32\notepad.exe'])

    elif 'stop' in className:
        speak('Stop sign detected. Setting an alarm.')
        exec(open("alarm.py").read())
        time.sleep(5)

    elif 'call me' in className:
        speak('Call me sign detected. Playing music.')
        music_dir = 'fav songs'
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))

    elif 'rock' in className:
        speak('Rock sign detected. Locking the screen.')
        ctypes.windll.user32.LockWorkStation()

    elif 'okay' in className:
        speak('Okay sign detected. Taking a screenshot.')
        time.sleep(5)
        now = datetime.datetime.now()
        filename = f"screenshot_{now.strftime('%Y-%m-%d-%H-%M-%S')}.png"
        pyautogui.screenshot(filename)
        speak('Screenshot taken.')

    elif 'smile' in className:
        speak('Smile sign detected. Here’s a joke for you.')
        joke = pyjokes.get_joke()
        print(joke)
        speak(joke)

    elif 'fist' in className:
        speak('Fist sign detected. Opening WPS Office.')
        # Example: Open Microsoft Word instead
        os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")  # Update path based on your software


    # Exit on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

    # Show output frame
    cv2.imshow("TELEX-HAND ASSISTANT", frame)

# Cleanup
cap.release()
cv2.destroyAllWindows()
'''