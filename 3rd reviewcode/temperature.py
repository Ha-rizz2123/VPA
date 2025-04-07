'''import requests
from bs4 import BeautifulSoup
import tkinter as tk
import pyttsx3 
import speech_recognition as sr

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()
    
def get_temperature():
    
    city = city_entry.get().lower()
    url = f"https://www.google.com/search?q=temperature+{city}"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    temp = soup.find("div", class_="BNeawe").text
    temp = temp.split(":")[-1].split()[0]
    text=f"The temperature in {city} is {temp}."
    
    result_label.config(text=f"The temperature in {city} is {temp}.")
    speak(text)
    
speak("Enter the city name in the label")
# create the GUI window
window = tk.Tk()
window.title("Temperature Retrieval")

# create the input label and entry widget for city
city_label = tk.Label(window, text="Enter city:")
city_entry = tk.Entry(window)
city_label.pack()
city_entry.pack()

# create the button widget to retrieve temperature
temp_button = tk.Button(window, text="Get Temperature", command=get_temperature)
temp_button.pack()

# create the label widget to display the temperature result
result_label = tk.Label(window, text="")
result_label.pack()

# start the GUI window
window.mainloop()'''
'''
import os
import requests
import tkinter as tk
import pyttsx3

# Load API key from environment variable
API_KEY = "b097cf9cea63057fd04eda4e69afeb84"
if not API_KEY:
    raise ValueError("API key is missing! Set the OPENWEATHER_API_KEY environment variable.")

# Initialize Text-to-Speech engine
engine = pyttsx3.init('sapi5')
engine.setProperty('voice', engine.getProperty('voices')[0].id)

def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()

def get_temperature():
    """Fetch temperature from OpenWeather API and update UI."""
    city = city_entry.get().strip()
    
    if not city:
        result_label.config(text="Please enter a city name.")
        speak("Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            text = f"The temperature in {city} is {temp}°C."
            result_label.config(text=text)
            speak(text)
        else:
            error_message = data.get("message", "Could not retrieve temperature.")
            result_label.config(text=error_message)
            speak(error_message)

    except requests.exceptions.RequestException:
        result_label.config(text="Network error. Please check your connection.")
        speak("Network error. Please check your connection.")

# Speak instruction at startup
speak("Enter the city name in the label")

# Create the GUI window
window = tk.Tk()
window.title("Weather App")
window.geometry("400x300")
window.configure(bg="lightblue")

# Create UI components
city_label = tk.Label(window, text="Enter city:", font=("Arial", 14), bg="lightblue")
city_entry = tk.Entry(window, font=("Arial", 14), width=20)
temp_button = tk.Button(window, text="Get Temperature", font=("Arial", 12), command=get_temperature)
result_label = tk.Label(window, text="", font=("Arial", 14), bg="lightblue")

# Arrange UI components with spacing
city_label.pack(pady=10)
city_entry.pack(pady=5)
temp_button.pack(pady=10)
result_label.pack(pady=10)

# Start the GUI event loop
window.mainloop()
'''

import requests
import tkinter as tk
import pyttsx3

# Load API Key
API_KEY = "b097cf9cea63057fd04eda4e69afeb84"

# Initialize Text-to-Speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def get_temperature():
    """Fetch temperature from OpenWeather API and update UI."""
    city = city_entry.get().strip()

    if not city:
        result_label.config(text="Please enter a city name.", fg="red")
        speak("Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"].capitalize()
            text = f"The temperature in {city} is {temp}°C with {weather_desc}."
            result_label.config(text=text, fg="black")
            speak(text)
        else:
            error_message = data.get("message", "Could not retrieve temperature.")
            result_label.config(text=error_message, fg="red")
            speak(error_message)

    except requests.exceptions.RequestException:
        result_label.config(text="Network error. Please check your connection.", fg="red")
        speak("Network error. Please check your connection.")

# Speak instruction at startup
speak("Welcome to the Weather App. Enter a city name to get the temperature.")

# Create GUI window
window = tk.Tk()
window.title("Weather App")
window.geometry("500x300")
window.configure(bg="#f0f0f0")

# Create a frame for better organization
main_frame = tk.Frame(window, bg="#f0f0f0", padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# UI Components with simpler styling
header_label = tk.Label(main_frame, text="Weather Temperature App", font=("Arial", 16, "bold"), bg="#f0f0f0")
header_label.pack(pady=(0, 20))

city_frame = tk.Frame(main_frame, bg="#f0f0f0")
city_frame.pack(pady=10)

city_label = tk.Label(city_frame, text="Enter City:", font=("Arial", 12), bg="#f0f0f0")
city_label.pack(side=tk.LEFT, padx=(0, 10))

city_entry = tk.Entry(city_frame, font=("Arial", 12), width=20)
city_entry.pack(side=tk.LEFT)

temp_button = tk.Button(main_frame, text="Get Temperature", font=("Arial", 12),
                        bg="#4CAF50", fg="white", padx=10, pady=5, command=get_temperature)
temp_button.pack(pady=20)

result_frame = tk.Frame(main_frame, bg="#f0f0f0", pady=10)
result_frame.pack(fill="x")

result_label = tk.Label(result_frame, text="Temperature results will appear here",
                        font=("Arial", 12), bg="#f0f0f0", wraplength=400)
result_label.pack()

# Run GUI
window.mainloop()
