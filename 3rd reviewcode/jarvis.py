'''import pyttsx3
import speech_recognition as sr
import datetime
import os
import openai
import wikipedia
import subprocess
import pywhatkit
import requests
from bs4 import BeautifulSoup
import pyautogui
import pyjokes
import webbrowser
import pyautogui
import datetime
import colorama
from colorama import Fore
import sys
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer,QTime,QDate
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from jarvisSuperUI import Ui_Form
import subprocess


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)


def speak(audio):
    
    engine.say(audio)
    engine.runAndWait()

class MainThread(QThread):
    def __init__(self):
        
        super(MainThread,self).__init__()
    
    def run(self):
        self.TaskExection()

    def commands(self):
     
        r = sr.Recognizer()
        with sr.Microphone() as source:
            
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source , duration=1)
            audio=r.listen(source)
        try:
            
            query = r.recognize_google(audio, language='en-in')
            print(f"You Just Said: {query}\n")
        except Exception as e:
            print(e)
            
            query="none"
        
        return query
      

    def wishings(self):
        hour = int(datetime.datetime.now().hour)
        if hour >=0 and hour<12:
            print("Good morning BOSS")
            speak('Good morning BOSS')
        elif hour>=12 and hour<17:
            print("Good Afternoon BOSS")
            speak("Good Afternoon BOSS")
        elif hour >=17 and hour<21:
            print("Good Evening BOSS")
            speak("Good Evening BOSS")
        else:
            print("Good Night BOSS")
            speak("Good Night BOSS")


    def TaskExection(self):
        
        def open_another_file(self):
         
            speak('you switched to hand sign mode')
            os.startfile("hand_assistant.py")
            
        self.wishings()
        while True:
            self.query = self.commands().lower()
            if 'time' in self.query:
                    strTime = datetime.datetime.now().strftime("%H:%M:%S")
                    speak("Sir, The time is: " + strTime)
                    print(strTime)
            elif 'question' in self.query or 'doubts' in self.query or 'question' in self.query or 'doubt' in self.query:
                    openai.api_key = "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"
                    speak('ask anything')
                    prompt = self.commands().lower()
                    if prompt in "none":
                       continue
                    print("Your query:", prompt)
                    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=2000)
                    a= response["choices"][0]["text"]
                    print(a)
                    speak(a)

            elif 'wikipedia' in self.query:
                speak("Searching in wikipedia")
                try:
                    self.query=self.query.replace("wikipedia", '')
                    results = wikipedia.summary(self.query, sentences=1)
                    speak("According to Wikipedia..")
                    print(results)
                    speak(results)
                except:
                    print("No results found..")
                    speak("no results found")

            elif 'play' in self.query:
                playquery=self.query.replace('play','')
                speak("Playing " + playquery)
                pywhatkit.playonyt(playquery)
            elif 'gmail' in self.query:
                speak('Opening Gmail....')
                url = "https://www.gmail.com"
                webbrowser.open_new_tab(url)
            elif 'youtube' in self.query:
                speak('Opening....')
                url = "https://www.youtube.com"
                webbrowser.open_new_tab(url)
            elif 'music' in self.query:
                speak('Playing')
                music_dir = 'fav songs'
                songs = os.listdir(music_dir)
                print(songs)    
                os.startfile(os.path.join(music_dir, songs[0]))       
                 
            elif 'temperature' in self.query:
                 speak('sure, Tell me the city')
                 print("Tell me the city")
                 city = self.commands().lower()
                 print(city)
                 url = f"https://www.google.com/search?q=temperature+{city}"
                 r = requests.get(url)
                 soup = BeautifulSoup(r.text, "html.parser")
                 temp = soup.find("div", class_="BNeawe").text
                 temp = temp.split(":")[-1].split()[0]
                 z= f"The temperature in {city} is {temp}."
                 print(z)
                 speak(z)            

            elif 'screenshot' in self.query:
                 speak('I am going to take Screenshot')
                 now = datetime.datetime.now()
                 filename = "screenshot{}.png".format(now.strftime("%Y-%m-%d-%H-%M-%S"))
                 pyautogui.screenshot(filename)
                 
            elif 'joke' in self.query:
                jarvisJoke = pyjokes.get_joke()
                print(jarvisJoke)
                speak(jarvisJoke)
            else:
                speak("please say the command again")

def open_another_file():
    speak('you switched to hand sign mode')
    try:
        subprocess.run(['python', 'hand_assistant.py'], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.startPushButton.clicked.connect(self.startTask)
        self.ui.quitPushButton.clicked.connect(open_another_file)

    def startTask(self, text):
        self.ui.movie = QtGui.QMovie("GUI files\\telex.jpeg")
        self.ui.ironManBackground.setMovie(self.ui.movie)
        self.ui.movie.start()
        # ironmanGIF
        self.ui.movie = QtGui.QMovie("GUI files\\listeningGIF.gif")
        self.ui.ironManGIF.setMovie(self.ui.movie)
        self.ui.movie.start()
        # dateLabel
        self.ui.movie = QtGui.QMovie("GUI files\\gggf.jpg")
        self.ui.dateLabel.setMovie(self.ui.movie)
        self.ui.movie.start()
        # timeLabel
        self.ui.movie = QtGui.QMovie("GUI files\\gggf.jpg")
        self.ui.timeLabel.setMovie(self.ui.movie)
        self.ui.movie.start()
        # startLabelNotButton
        self.ui.movie = QtGui.QMovie("GUI files\\20230401_185949_0000.png")
        self.ui.startLabelNotButton.setMovie(self.ui.movie)
        self.ui.movie.start()
        # quitLabelNotButton
        self.ui.movie = QtGui.QMovie("GUI files\\20230401_191740_0000.png")
        self.ui.quitLabelNotButton.setMovie(self.ui.movie)
        self.ui.movie.start()
        # earthGIF
        self.ui.movie = QtGui.QMovie("GUI files\\Earth.gif")
        self.ui.earthGIF.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("GUI files\\initial.gif")
        self.ui.jarvisGUI.setMovie(self.ui.movie)
        self.ui.movie.start()

        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()
        labelTime = currentTime.toString('hh:mm:ss')
        labelDate = currentDate.toString(Qt.ISODate)
        self.ui.dateTextBrowser.setText(f"Date: {labelDate}")
        self.ui.timeTextBrowser.setText(f"Time: {labelTime}")
    

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
'''      
'''
import pyttsx3
import speech_recognition as sr
import datetime
import os
import openai
import wikipedia
import subprocess
import pywhatkit
import requests
from bs4 import BeautifulSoup
import pyautogui
import pyjokes
import webbrowser
import sys
from PyQt5.QtCore import QThread, QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from jarvisSuperUI import Ui_Form

# Set working directory to script location
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"✅ Working Directory Set: {os.getcwd()}")

# Initialize speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# Safe speak function to avoid "run loop already started" error
def speak(audio):
    if not engine._inLoop:
        engine.say(audio)
        engine.runAndWait()
    else:
        engine.say(audio)

# Background thread for voice assistant tasks
class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def commands(self):
     r = sr.Recognizer()
     with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    
     try:
        query = r.recognize_google(audio, language='en-in')
        print(f"✅ You said: {query}")  # Debugging print
     except sr.UnknownValueError:
        print("❌ I couldn't understand. Please repeat.")
        query = "none"
     except sr.RequestError:
        print("❌ Error: Could not connect to Google Speech Recognition.")
        query = "none"
    
     return query.lower()


    def wishings(self):
        hour = int(datetime.datetime.now().hour)
        if hour < 12:
            speak('Good morning BOSS')
        elif hour < 17:
            speak("Good Afternoon BOSS")
        elif hour < 21:
            speak("Good Evening BOSS")
        else:
            speak("Good Night BOSS")

    def TaskExecution(self):
        self.wishings()
        while True:
            query = self.commands()
            if 'time' in query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                speak("Sir, The time is: " + strTime)
                print(strTime)
            elif 'wikipedia' in query:
                speak("Searching Wikipedia...")
                try:
                    query = query.replace("wikipedia", "")
                    results = wikipedia.summary(query, sentences=1)
                    speak("According to Wikipedia..")
                    print(results)
                    speak(results)
                except:
                    speak("No results found.")
            elif 'play' in query:
                play_query = query.replace('play', '')
                speak("Playing " + play_query)
                pywhatkit.playonyt(play_query)
            elif 'gmail' in query:
                webbrowser.open_new_tab("https://www.gmail.com")
            elif 'youtube' in query:
                webbrowser.open_new_tab("https://www.youtube.com")
            elif 'joke' in query:
                joke = pyjokes.get_joke()
                print(joke)
                speak(joke)
            elif 'temperature' in query:
                speak('Tell me the city')
                city = self.commands()
                url = f"https://www.google.com/search?q=temperature+{city}"
                r = requests.get(url)
                soup = BeautifulSoup(r.text, "html.parser")
                temp = soup.find("div", class_="BNeawe").text
                speak(f"The temperature in {city} is {temp}.")
            elif 'screenshot' in query:
                speak('Taking a screenshot')
                now = datetime.datetime.now()
                filename = f"screenshot_{now.strftime('%Y-%m-%d-%H-%M-%S')}.png"
                pyautogui.screenshot(filename)
            else:
                speak("Please say the command again.")

# Function to open `hand_assistant.py`
def open_another_file():
    hand_assistant_path = os.path.join(os.getcwd(), "hand_assistant.py")
    print(f"🔍 Checking: {hand_assistant_path}")

    if os.path.exists(hand_assistant_path):
        print("✅ hand_assistant.py found! Running it now...")
        speak('Switching to hand sign mode...')
        subprocess.run(['python', hand_assistant_path], check=True)
    else:
        print(f"❌ Error: 'hand_assistant.py' NOT FOUND at {hand_assistant_path}!")

# Initialize voice assistant thread
startExecution = MainThread()

# Main GUI class
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Connect buttons
        self.ui.startPushButton.clicked.connect(self.startTask)
        self.ui.quitPushButton.clicked.connect(open_another_file)

        # Start time updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)  # Update every second

    def startTask(self):
        """Start animations and voice assistant."""
        self.loadGif("initial.gif", self.ui.jarvisGUI)
        self.loadGif("listeningGIF.gif", self.ui.ironManGIF)
        self.loadGif("Earth.gif", self.ui.earthGIF)
        self.loadImage("telex.gif", self.ui.ironManBackground)  # Updated from telex.jpeg to telex.gif
        self.loadImage("gggf.jpg", self.ui.dateLabel)
        self.loadImage("gggf.jpg", self.ui.timeLabel)
        self.loadImage("20230401_185949_0000.png", self.ui.startLabelNotButton)
        self.loadImage("20230401_191740_0000.png", self.ui.quitLabelNotButton)

        startExecution.start()

    def showTime(self):
        """Update date and time dynamically."""
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()
        labelTime = currentTime.toString("hh:mm:ss")
        labelDate = currentDate.toString(Qt.ISODate)  # Fixed import issue
        self.ui.dateTextBrowser.setText(f"Date: {labelDate}")
        self.ui.timeTextBrowser.setText(f"Time: {labelTime}")

    def loadGif(self, file_name, widget):
        """Load a GIF file into a QLabel."""
        file_path = os.path.join(os.getcwd(), "GUI files", file_name)
        if os.path.exists(file_path):
            movie = QMovie(file_path)
            widget.setMovie(movie)
            movie.start()
        else:
            print(f"❌ Error: GIF not found - {file_path}")

    def loadImage(self, file_name, widget):
        """Load an image file into a QLabel."""
        file_path = os.path.join(os.getcwd(), "GUI files", file_name)
        if os.path.exists(file_path):
            pixmap = QPixmap(file_path)
            widget.setPixmap(pixmap)
        else:
            print(f"❌ Error: Image not found - {file_path}")

# Run the application
app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
sys.exit(app.exec_())
'''


'''
import threading
import speech_recognition as sr
import pyttsx3
import datetime
import os
import wikipedia
import pywhatkit
import sys
import webbrowser
import subprocess
from PyQt5.QtCore import QThread, QTimer, QTime, QDate, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from jarvisSuperUI import Ui_Form
import os

import pyautogui
import pyjokes
import ctypes
import subprocess

# ✅ Set working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"✅ Working Directory Set: {os.getcwd()}")

# ✅ Initialize Text-to-Speech Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ✅ Speak Function (Fixed for Multithreading)
def speak(text):
    print(f"🗣️ Speaking: {text}")
    engine.stop()  
    engine.say(text)
    engine.runAndWait()

# ✅ Speech Recognition Thread
class SpeechRecognitionThread(QThread):
    recognized_signal = pyqtSignal(str)  

    def __init__(self):
        super().__init__()
        self.r = sr.Recognizer()
        self.mic_index = 1  
        self.running = True  

    def run(self):
        print("🎤 Speech Recognition Thread Started.")
        while self.running:
            query = self.listen_for_commands()
            if query in ["exit", "quit", "stop"]:
                print("🛑 Exit command received. Stopping Jarvis...")
                self.recognized_signal.emit("Goodbye! Shutting down.")  
                self.running = False  
                break  
            elif query != "none":
                self.recognized_signal.emit(query)  

    def listen_for_commands(self):
        try:
            with sr.Microphone(device_index=self.mic_index) as source:
                print("🎤 Listening... Speak now!")
                self.r.adjust_for_ambient_noise(source, duration=2)  
                audio = self.r.listen(source, timeout=10, phrase_time_limit=10)

            query = self.r.recognize_google(audio, language='en-IN')
            print(f"✅ Recognized: {query}")
            return query.lower()

        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return "none"
        except sr.RequestError:
            print("❌ Google Speech API is not reachable.")
            return "none"
        except sr.WaitTimeoutError:
            print("⏳ Timeout: No speech detected.")
            return "none"

    def stop(self):
        """ Stop the speech recognition thread """
        print("🛑 Stopping Speech Recognition Thread...")
        self.running = False

# ✅ Main Thread for Jarvis AI
class MainThread(QThread):
    recognized_signal = pyqtSignal(str)  

    def __init__(self):
        super(MainThread, self).__init__()
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.recognized_signal.connect(self.process_command)  

    def run(self):
        print("🚀 Running Jarvis Voice Assistant...")
        self.speech_thread.start()
        self.wishings()

    def wishings(self):
        """ Greet the user based on the time of day. """
        hour = int(datetime.datetime.now().hour)
        if hour < 12:
            self.recognized_signal.emit("Good morning BOSS")
        elif hour < 17:
            self.recognized_signal.emit("Good Afternoon BOSS")
        elif hour < 21:
            self.recognized_signal.emit("Good Evening BOSS")
        else:
            self.recognized_signal.emit("Good Night BOSS")

    def process_command(self, query):
        print(f"✅ Processing Command: {query}")

        if query == "none":
            return  

        if "time" in query or "current time" in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")  
            self.recognized_signal.emit(f"Sir, The time is {strTime}")
            print(f"⌚ Time: {strTime}")  

        elif "date" in query or "today's date" in query:
            current_date = datetime.datetime.now().strftime("%A, %d %B %Y")  
            self.recognized_signal.emit(f"Sir, today's date is {current_date}")
            print(f"📅 Date: {current_date}")

        elif "wikipedia" in query:
            self.recognized_signal.emit("Searching Wikipedia...")
            try:
                search_term = query.replace("wikipedia", "").strip()
                results = wikipedia.summary(search_term, sentences=2)
                self.recognized_signal.emit(results)
                print(f"📖 Wikipedia: {results}")
            except wikipedia.exceptions.DisambiguationError:
                self.recognized_signal.emit("There are multiple results. Please be more specific.")
            except wikipedia.exceptions.PageError:
                self.recognized_signal.emit("No results found for your search.")

        elif "play" in query:
            song = query.replace("play", "").strip()
            self.recognized_signal.emit(f"Playing {song} on YouTube")
            pywhatkit.playonyt(song)

        elif "exit" in query or "quit" in query or "stop" in query:
            print("🛑 Exit command received. Stopping Jarvis...")
            self.recognized_signal.emit("Goodbye! Shutting down.")
            self.speech_thread.stop()
            sys.exit(0)  

        else:
            self.recognized_signal.emit("I didn't understand. Please try again.")

    def process_command(query):
        """ Process voice commands (mapped from hand gestures) """

        # ✅ TEMPERATURE CHECK (Victory Sign)
        if "temperature" in query:
            speak("Checking temperature...")
            exec(open("temperature.py").read())

        # ✅ ACTIVATE CHATGPT (Thumbs Down)
        elif "chatgpt" in query:
            speak("Activating ChatGPT...")
            exec(open("chatgpt.py").read())

        # ✅ OPEN GMAIL (Live Long)
        elif "open gmail" in query:
            speak("Opening Gmail...")
            webbrowser.open_new_tab("https://www.gmail.com")

        # ✅ OPEN NOTEPAD (Thumbs Up)
        elif "open notepad" in query:
            speak("Opening Notepad...")
            subprocess.run(["notepad.exe"])

        # ✅ SET ALARM (Stop Sign)
        elif "set an alarm" in query:
            speak("Setting an alarm...")
            exec(open("alarm.py").read())

        # ✅ PLAY MUSIC (Call Me)
        elif "play music" in query:
            speak("Playing your favorite music.")
            music_dir = "fav songs"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        # ✅ LOCK SCREEN (Rock Sign)
        elif "lock my screen" in query:
            speak("Locking your screen.")
                ctypes.windll.user32.LockWorkStation()

        # ✅ TAKE A SCREENSHOT (Okay Sign)
        elif "take a screenshot" in query:
            speak("Taking a screenshot in 5 seconds.")
                time.sleep(5)
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"
                pyautogui.screenshot(filename)
            speak("Screenshot saved.")

        # ✅ TELL A JOKE (Smile Sign)
        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        # ✅ OPEN WPS OFFICE (Fist Sign)
        elif "open wps office" in query:
            speak("Opening WPS Office.")
            os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")

        else:
            speak("I didn't understand. Please try again.")

# ✅ Function to Open Hand Sign Mode
def open_hand_sign_mode():
    print("🔄 Switching to Hand Sign Mode...")
    speak("Switching to Hand Sign Mode")
    os.system("python hand_assistant.py")  

# ✅ GUI Class
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.startPushButton.clicked.connect(self.startTask)
        self.ui.quitPushButton.clicked.connect(open_hand_sign_mode)  # ✅ Hand Sign Mode Button

        startExecution.recognized_signal.connect(self.handle_recognition)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

    def startTask(self):
        print("✅ Start Button Pressed - Running Jarvis AI")
        startExecution.start()

    def showTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()
        self.ui.dateTextBrowser.setText(f"Date: {currentDate.toString(Qt.ISODate)}")
        self.ui.timeTextBrowser.setText(f"Time: {currentTime.toString('hh:mm:ss')}")

    def handle_recognition(self, text):
        speak(text)

# ✅ Start Voice Assistant Thread
startExecution = MainThread()

# ✅ Run the GUI
app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
sys.exit(app.exec_())
'''

import threading
import speech_recognition as sr
import pyttsx3
import datetime
import os
import wikipedia
import pywhatkit
import sys
import webbrowser
import subprocess
import pyautogui
import pyjokes
import ctypes
import time
from PyQt5.QtCore import QThread, QTimer, QTime, QDate, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow
from jarvisSuperUI import Ui_Form

# ✅ Set working directory
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
print(f"✅ Working Directory Set: {os.getcwd()}")

# ✅ Initialize Text-to-Speech Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

# ✅ Speak Function
def speak(text):
    """ Speak text using TTS engine """
    print(f"🗣️ Speaking: {text}")
    engine.stop()  
    engine.say(text)
    engine.runAndWait()

# ✅ Speech Recognition Thread
class SpeechRecognitionThread(QThread):
    recognized_signal = pyqtSignal(str)  

    def __init__(self):
        super().__init__()
        self.r = sr.Recognizer()
        self.mic_index = 1  
        self.running = True  

    def run(self):
        print("🎤 Speech Recognition Thread Started.")
        while self.running:
            query = self.listen_for_commands()
            if query in ["exit", "quit", "stop"]:
                print("🛑 Exit command received. Stopping Jarvis...")
                self.recognized_signal.emit("Goodbye! Shutting down.")  
                self.running = False  
                break  
            elif query != "none":
                self.recognized_signal.emit(query)  

    def listen_for_commands(self):
        try:
            with sr.Microphone(device_index=self.mic_index) as source:
                print("🎤 Listening... Speak now!")
                self.r.adjust_for_ambient_noise(source, duration=2)  
                audio = self.r.listen(source, timeout=10, phrase_time_limit=10)

            query = self.r.recognize_google(audio, language='en-IN')
            print(f"✅ Recognized: {query}")
            return query.lower()

        except sr.UnknownValueError:
            print("❌ Could not understand audio.")
            return "none"
        except sr.RequestError:
            print("❌ Google Speech API is not reachable.")
            return "none"
        except sr.WaitTimeoutError:
            print("⏳ Timeout: No speech detected.")
            return "none"

    def stop(self):
        """ Stop the speech recognition thread """
        print("🛑 Stopping Speech Recognition Thread...")
        self.running = False

# ✅ Main Thread for Jarvis AI

class MainThread(QThread):
    recognized_signal = pyqtSignal(str)  

    def __init__(self):
        super(MainThread, self).__init__()
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.recognized_signal.connect(self.process_command)  

    def run(self):
        print("🚀 Running Jarvis Voice Assistant...")
        self.speech_thread.start()
        self.wishings()

    def wishings(self):
        """ Greet the user based on the time of day. """
        hour = int(datetime.datetime.now().hour)
        if hour < 12:
            self.recognized_signal.emit("Good morning BOSS")
        elif hour < 17:
            self.recognized_signal.emit("Good Afternoon BOSS")
        elif hour < 21:
            self.recognized_signal.emit("Good Evening BOSS")
        else:
            self.recognized_signal.emit("Good Night BOSS")

    def process_command(self, query):
        """ Process voice commands (mapped from hand gestures) """
        print(f"✅ Processing Command: {query}")

        if query == "none":
            return  

        if "time" in query or "current time" in query:
            strTime = datetime.datetime.now().strftime("%I:%M %p")  
            speak(f"Sir, The time is {strTime}")
            print(f"⌚ Time: {strTime}")  

        elif "date" in query or "today's date" in query:
            current_date = datetime.datetime.now().strftime("%A, %d %B %Y")  
            speak(f"Sir, today's date is {current_date}")
            print(f"📅 Date: {current_date}")

        elif "temperature" in query:
            speak("Checking temperature...")
            subprocess.Popen(["python", "temperature.py"])

        elif "chatgpt" in query:
            speak("Activating ChatGPT...")
            subprocess.Popen(["python", "chatgpt.py"])

        elif "open gmail" in query:
            speak("Opening Gmail...")
            webbrowser.open_new_tab("https://www.gmail.com")

        elif "open notepad" in query:
            speak("Opening Notepad...")
            subprocess.run(["notepad.exe"])

        elif "set an alarm" in query:
            speak("Setting an alarm...")
            subprocess.Popen(["python", "alarm.py"])

        elif "play music" in query:
            speak("Playing your favorite music.")
            music_dir = "fav songs"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif "lock my screen" in query:
            speak("Locking your screen.")
            ctypes.windll.user32.LockWorkStation()

        elif "take a screenshot" in query:
            speak("Taking a screenshot in 5 seconds.")
            time.sleep(5)
            filename = f"screenshot_{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.png"
            pyautogui.screenshot(filename)
            speak("Screenshot saved.")

        elif "tell me a joke" in query:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "open wps office" in query:
            speak("Opening WPS Office.")
            os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")

        elif "exit" in query or "quit" in query or "stop" in query:
            print("🛑 Exit command received. Stopping Jarvis...")
            speak("Goodbye! Shutting down.")
            self.speech_thread.stop()
            sys.exit(0)  

        else:
            speak("I didn't understand. Please try again.")

# ✅ Function to Open Hand Sign Mode
def open_hand_sign_mode():
    print("🔄 Switching to Hand Sign Mode...")
    speak("Switching to Hand Sign Mode")
    subprocess.Popen(["python", "hand_assistant.py"])

# ✅ GUI Class
class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.startPushButton.clicked.connect(self.startTask)
        self.ui.quitPushButton.clicked.connect(open_hand_sign_mode)  

        startExecution.recognized_signal.connect(self.handle_recognition)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.showTime)
        self.timer.start(1000)

    def startTask(self):
        print("✅ Start Button Pressed - Running Jarvis AI")
        startExecution.start()

    def showTime(self):
        currentTime = QTime.currentTime()
        currentDate = QDate.currentDate()
        self.ui.dateTextBrowser.setText(f"Date: {currentDate.toString(Qt.ISODate)}")
        self.ui.timeTextBrowser.setText(f"Time: {currentTime.toString('hh:mm:ss')}")

    def handle_recognition(self, text):
        speak(text)

# ✅ Start Voice Assistant Thread
startExecution = MainThread()

# ✅ Run the GUI
app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
sys.exit(app.exec_())

