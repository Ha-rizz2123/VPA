import speech_recognition as sr
import pyttsx3
import datetime
import os
import sys

# ✅ Initialize Speech Recognition & TTS
r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    """ Convert text to speech """
    print(f"🗣️ Speaking: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """ Listen for voice commands """
    with sr.Microphone() as source:
        print("🎤 Listening... Speak now!")
        r.adjust_for_ambient_noise(source, duration=2)
        try:
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
            command = r.recognize_google(audio, language="en-IN")
            print(f"✅ Recognized: {command}")
            return command.lower()
        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return "none"
        except sr.RequestError:
            print("❌ Error connecting to Google Speech API.")
            return "none"

def execute_command(command):
    """ Perform actions based on recognized voice command """
    if "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {current_time}")
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today's date is {current_date}")
    elif "exit" in command or "quit" in command:
        speak("Goodbye! Shutting down.")
        sys.exit()
    else:
        speak("I didn't understand. Please try again.")

# ✅ Main Loop
if __name__ == "__main__":
    speak("Hello! I am your assistant. How can I help?")
    
    while True:
        user_command = listen()
        execute_command(user_command)
