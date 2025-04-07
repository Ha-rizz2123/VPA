import cv2
import numpy as np
import pyttsx3
import webbrowser
import os
import ctypes
import pyautogui
import mediapipe as mp
import datetime
import time
import pyjokes

# Initialize text-to-speech
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 150)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# Startup messages
speak('Hi, I am Telex. You can assist me using hand signs.')
print("=== TELEX HAND GESTURE ASSISTANT ===")
print("Available gestures:")
print("- Peace sign: Opens temperature app")
print("- Thumbs down: Opens ChatGPT app")
print("- Thumbs up: Opens Notepad")
print("- Stop sign: Opens alarm app")
print("- Call me sign: Plays music")
print("- Live long sign: Opens Gmail")
print("- Rock sign: Locks screen")
print("- Okay sign: Takes screenshot")
print("- Smile sign: Tells a joke")
print("- Fist sign: Opens Microsoft Word")
print("Press 'q' to quit the application")

# Initialize MediaPipe Hand Detection with improved parameters
mpHands = mp.solutions.hands
# Increase min_detection_confidence for more stable detection
# Add min_tracking_confidence to help with continuous tracking
hands = mpHands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mpDraw = mp.solutions.drawing_utils
# Create simple drawing specs instead of using the default styles
landmark_drawing_spec = mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2)
connection_drawing_spec = mp.solutions.drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=2)

# Initialize the webcam with specific resolution for better performance
cap = cv2.VideoCapture(0)
# Try to set resolution to 640x480 for better performance
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
# Try to set focus to auto if available
cap.set(cv2.CAP_PROP_AUTOFOCUS, 1)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    speak("Error: Could not open webcam.")
    exit()

def run_script(script_name):
    """Run an external Python script in a separate process to avoid conflicts."""
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(current_dir, script_name)

    if os.path.exists(script_path):
        try:
            # Use os.system to run the script in a separate process
            # This is more reliable than exec() which can cause namespace conflicts
            print(f"Running {script_name}...")
            os.system(f'python "{script_path}"')
        except Exception as e:
            print(f"Error executing {script_name}: {str(e)}")
            speak(f"Error executing {script_name}")
    else:
        # Try the simplified version if the original script is not found
        simple_name = script_name.replace('.py', '_simple.py')
        simple_path = os.path.join(current_dir, simple_name)

        if os.path.exists(simple_path):
            try:
                print(f"Running simplified version: {simple_name}...")
                os.system(f'python "{simple_path}"')
            except Exception as e:
                print(f"Error executing {simple_name}: {str(e)}")
                speak(f"Error executing simplified version")
        else:
            print(f"Error: {script_name} not found")
            speak(f"Error: {script_name} not found")

# Variables for gesture detection stability
last_gesture = None
gesture_counter = 0
GESTURE_THRESHOLD = 5  # Reduced threshold for faster response (was 10)
last_action_time = time.time()
ACTION_COOLDOWN = 2  # Reduced cooldown period (was 3)

while True:
    # Read each frame from the webcam
    ret, frame = cap.read()
    if not ret:
        print("Error: Unable to capture video.")
        break

    # Get frame dimensions correctly
    height, width, c = frame.shape
    frame = cv2.flip(frame, 1)  # Flip the frame horizontally
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    className = ''
    current_gesture = None

    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # Use width for x and height for y (corrected)
                lmx = int(lm.x * width)
                lmy = int(lm.y * height)
                landmarks.append([lmx, lmy])

            # Draw landmarks with custom style for better visibility
            mpDraw.draw_landmarks(
                frame,
                handslms,
                mpHands.HAND_CONNECTIONS,
                landmark_drawing_spec=landmark_drawing_spec,
                connection_drawing_spec=connection_drawing_spec
            )

            # Rule-based gesture detection
            if len(landmarks) >= 21:
                thumb_tip = landmarks[4]
                index_tip = landmarks[8]
                middle_tip = landmarks[12]
                ring_tip = landmarks[16]
                pinky_tip = landmarks[20]
                wrist = landmarks[0]

                # Get finger base positions for better reference
                index_base = landmarks[5]
                middle_base = landmarks[9]
                ring_base = landmarks[13]
                pinky_base = landmarks[17]

                # Peace sign - index and middle fingers up, others down
                if (index_tip[1] < index_base[1] and middle_tip[1] < middle_base[1] and
                    ring_tip[1] > ring_base[1] and pinky_tip[1] > pinky_base[1]):
                    current_gesture = "peace"
                    className = "peace"

                # Thumbs down
                elif thumb_tip[1] > wrist[1] and thumb_tip[0] > index_tip[0]:
                    current_gesture = "thumbs down"
                    className = "thumbs down"

                # Thumbs up
                elif thumb_tip[1] < wrist[1] and thumb_tip[0] < index_tip[0]:
                    current_gesture = "thumbs up"
                    className = "thumbs up"

                # Stop sign - all fingers up
                elif (index_tip[1] < index_base[1] and middle_tip[1] < middle_base[1] and
                      ring_tip[1] < ring_base[1] and pinky_tip[1] < pinky_base[1] and
                      thumb_tip[1] < wrist[1]):
                    current_gesture = "stop"
                    className = "stop"

                # Call me sign - thumb and pinky extended
                elif (thumb_tip[1] < wrist[1] and pinky_tip[1] < pinky_base[1] and
                      index_tip[1] > index_base[1] and middle_tip[1] > middle_base[1] and
                      ring_tip[1] > ring_base[1]):
                    current_gesture = "call me"
                    className = "call me"

                # Live long sign - index and middle together, ring and pinky together
                elif (index_tip[1] < index_base[1] and middle_tip[1] < middle_base[1] and
                      ring_tip[1] < ring_base[1] and pinky_tip[1] < pinky_base[1] and
                      abs(index_tip[0] - middle_tip[0]) < 50 and abs(ring_tip[0] - pinky_tip[0]) < 50 and
                      abs(middle_tip[0] - ring_tip[0]) > 50):
                    current_gesture = "live long"
                    className = "live long"

                # Rock sign - index and pinky extended, others closed
                elif (index_tip[1] < index_base[1] and pinky_tip[1] < pinky_base[1] and
                      middle_tip[1] > middle_base[1] and ring_tip[1] > ring_base[1]):
                    current_gesture = "rock"
                    className = "rock"

                # Okay sign - thumb and index form a circle
                elif (abs(thumb_tip[0] - index_tip[0]) < 50 and
                      abs(thumb_tip[1] - index_tip[1]) < 50 and
                      middle_tip[1] < middle_base[1]):
                    current_gesture = "okay"
                    className = "okay"

                # Smile sign - thumb extended to side
                elif (thumb_tip[0] > wrist[0] + 100 and
                      index_tip[1] > index_base[1] and middle_tip[1] > middle_base[1] and
                      ring_tip[1] > ring_base[1] and pinky_tip[1] > pinky_base[1]):
                    current_gesture = "smile"
                    className = "smile"

                # Fist sign - all fingers closed
                elif (index_tip[1] > index_base[1] and middle_tip[1] > middle_base[1] and
                      ring_tip[1] > ring_base[1] and pinky_tip[1] > pinky_base[1] and
                      thumb_tip[0] < index_base[0]):
                    current_gesture = "fist"
                    className = "fist"

    # Gesture stability logic
    if current_gesture == last_gesture and current_gesture is not None:
        gesture_counter += 1
    else:
        gesture_counter = 0
        last_gesture = current_gesture

    # Execute action only if gesture is stable and cooldown period has passed
    current_time = time.time()
    if gesture_counter >= GESTURE_THRESHOLD and (current_time - last_action_time) > ACTION_COOLDOWN:
        # Reset counter and update last action time
        gesture_counter = 0
        last_action_time = current_time

        # Execute the corresponding action based on the gesture
        if current_gesture == "peace":
            speak("Temperature app detected")
            run_script("temperature.py")
        elif current_gesture == "thumbs down":
            speak("ChatGPT app detected")
            run_script("chatgpt.py")
        elif current_gesture == "thumbs up":
            speak("Opening notepad")
            os.system('notepad.exe')
        elif current_gesture == "stop":
            speak("Alarm app detected")
            run_script("alarm.py")
        elif current_gesture == "call me":
            speak("Playing music")
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            music_dir = os.path.join(current_dir, 'fav songs')
            if os.path.exists(music_dir) and os.listdir(music_dir):
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[0]))
            else:
                speak("No music files found in the favorites folder")
        elif current_gesture == "live long":
            speak('Live long sign detected, opening Gmail')
            webbrowser.open_new_tab("https://www.gmail.com")
        elif current_gesture == "rock":
            speak('Rock sign detected, locking screen')
            ctypes.windll.user32.LockWorkStation()
        elif current_gesture == "okay":
            speak('Okay sign detected, taking screenshot')
            now = datetime.datetime.now()
            filename = f"screenshot_{now.strftime('%Y-%m-%d-%H-%M-%S')}.png"
            pyautogui.screenshot(filename)
        elif current_gesture == "smile":
            speak('Smile sign detected, here is a joke for you')
            joke = pyjokes.get_joke()
            speak(joke)
        elif current_gesture == "fist":
            speak('Fist sign detected, opening Microsoft Word')
            os.startfile(r"C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE")

    # Show the prediction and status on the frame
    cv2.putText(frame, f"Gesture: {className}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA)

    # Show stability counter if a gesture is being detected
    if current_gesture is not None:
        stability = min(gesture_counter / GESTURE_THRESHOLD * 100, 100)
        cv2.putText(frame, f"Stability: {stability:.0f}%", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA)

    # Show cooldown timer if applicable
    time_since_last = time.time() - last_action_time
    if time_since_last < ACTION_COOLDOWN:
        cooldown = ACTION_COOLDOWN - time_since_last
        cv2.putText(frame, f"Cooldown: {cooldown:.1f}s", (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA)

    # Show finger positions for debugging (if landmarks are detected)
    if result.multi_hand_landmarks and len(landmarks) >= 21:
        finger_tips = [
            ("Thumb", landmarks[4][1] < landmarks[0][1]),
            ("Index", landmarks[8][1] < landmarks[5][1]),
            ("Middle", landmarks[12][1] < landmarks[9][1]),
            ("Ring", landmarks[16][1] < landmarks[13][1]),
            ("Pinky", landmarks[20][1] < landmarks[17][1])
        ]

        # Display which fingers are up
        fingers_text = "Fingers up: " + ", ".join([name for name, is_up in finger_tips if is_up])
        cv2.putText(frame, fingers_text, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 0), 2, cv2.LINE_AA)

    # Instructions
    cv2.putText(frame, "Press 'q' to quit", (width - 200, height - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("TELEX-HAND ASSISTANT", frame)
    # Exit on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
