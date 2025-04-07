'''import openai
import tkinter as tk
import pyttsx3

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
engine.setProperty('rate', 150)
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

openai.api_key ="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"
def generate_response():
    
    prompt = query.get()
    
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=2000)
    answer = response["choices"][0]["text"]
    print(answer)
    speak(answer)
    answer_label.config(text=answer)
    

root = tk.Tk()
root.title("ASK ME ANYTHING")

# create query entry widget
query = tk.Entry(root, width=50, font=("Helvetica", 14))
query.pack(pady=10)

# create generate button
generate_button = tk.Button(root, text="SEARCH", command=generate_response)
generate_button.pack(pady=10)

# create answer label
answer_label = tk.Label(root, text="", font=("Helvetica", 14))
answer_label.pack(pady=10)

root.mainloop()

'''
'''
import requests
import tkinter as tk
from tkinter import messagebox

# Set your Hugging Face API key (Replace with your actual key)
HUGGINGFACE_API_KEY = "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"

# ✅ Use a working Hugging Face model
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"

def generate_response():
    """Fetch AI-generated response from Hugging Face API and display it."""
    user_input = query_entry.get().strip()

    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": user_input,
        "parameters": {"max_length": 200}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response_data = response.json()

        # Handling potential errors in the response
        if response.status_code != 200:
            error_message = response_data.get("error", "Unknown error")
            answer_label.config(text=f"Error: {error_message}")
            return

        # Extract generated text from response
        if isinstance(response_data, list) and len(response_data) > 0 and "generated_text" in response_data[0]:
            bot_reply = response_data[0]["generated_text"]
            answer_label.config(text=bot_reply, wraplength=400, justify="left")
        else:
            answer_label.config(text="Error: No valid response received")

    except Exception as e:
        messagebox.showerror("API Error", f"Failed to get response: {e}")

# GUI Setup
root = tk.Tk()
root.title("Hugging Face Chatbot")
root.geometry("500x300")

# Query Entry
query_entry = tk.Entry(root, width=50, font=("Helvetica", 14))
query_entry.pack(pady=10)

# Generate Button
generate_button = tk.Button(root, text="Generate", command=generate_response, font=("Helvetica", 12), bg="#4CAF50", fg="white")
generate_button.pack(pady=10)

# Answer Label
answer_label = tk.Label(root, text="", font=("Helvetica", 14), wraplength=400, justify="left")
answer_label.pack(pady=10)

# Run Tkinter
root.mainloop()
'''
'''
import requests
import tkinter as tk
from tkinter import messagebox
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# Set your Hugging Face API key (Replace with your actual key)
HUGGINGFACE_API_KEY = "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"

# ✅ Use a working Hugging Face model
API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"


def generate_response():
    """Fetch AI-generated response from Hugging Face API and display it with voice output."""
    user_input = query_entry.get().strip()

    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": user_input,
        "parameters": {"max_length": 50, "temperature": 0.7, "top_p": 0.9}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response_data = response.json()

        # Handling potential errors in the response
        if response.status_code != 200:
            error_message = response_data.get("error", "Unknown error")
            answer_label.config(text=f"Error: {error_message}", fg="red")
            return

        # Extract generated text from response
        if isinstance(response_data, list) and len(response_data) > 0 and "generated_text" in response_data[0]:
            bot_reply = response_data[0]["generated_text"]
            answer_label.config(text=bot_reply, wraplength=400, justify="left", fg="black")
            speak(bot_reply)  # Speak the generated response
        else:
            answer_label.config(text="Error: No valid response received", fg="red")

    except Exception as e:
        messagebox.showerror("API Error", f"Failed to get response: {e}")

# GUI Setup with Improved Design
root = tk.Tk()
root.title("AI Chatbot - Hugging Face")
root.geometry("600x400")
root.configure(bg="#F0F0F0")

# Heading
heading_label = tk.Label(root, text="Hugging Face Chatbot", font=("Helvetica", 18, "bold"), bg="#F0F0F0", fg="#333")
heading_label.pack(pady=10)

# Query Entry
query_entry = tk.Entry(root, width=50, font=("Helvetica", 14), bd=2, relief="solid")
query_entry.pack(pady=10)

# Generate Button
generate_button = tk.Button(root, text="Generate Response", command=generate_response, font=("Helvetica", 12, "bold"), 
                            bg="#4CAF50", fg="white", padx=20, pady=5)
generate_button.pack(pady=10)

# Answer Label
answer_label = tk.Label(root, text="", font=("Helvetica", 14), bg="#F0F0F0", fg="black", wraplength=500, justify="left")
answer_label.pack(pady=20)

# Run Tkinter
root.mainloop()'''

'''
import requests
import tkinter as tk
from tkinter import messagebox, PhotoImage
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# Set your Hugging Face API key (Replace with your actual key)
HUGGINGFACE_API_KEY = "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"

# ✅ Use a working Hugging Face model
API_URL = "https://api-inference.huggingface.co/models/facebook/opt-1.3b"

def generate_response():
    """Fetch AI-generated response from Hugging Face API and display it with voice output."""
    user_input = query_entry.get().strip()

    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": user_input,
        "parameters": {"max_length": 50, "temperature": 0.7, "top_p": 0.9}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response_data = response.json()

        # Handling potential errors in the response
        if response.status_code != 200:
            error_message = response_data.get("error", "Unknown error")
            answer_label.config(text=f"Error: {error_message}", fg="red")
            return

        # Extract generated text from response
        if isinstance(response_data, list) and len(response_data) > 0 and "generated_text" in response_data[0]:
            bot_reply = response_data[0]["generated_text"]
            answer_label.config(text=bot_reply, wraplength=400, justify="left", fg="black")
            speak(bot_reply)  # Speak the generated response
        else:
            answer_label.config(text="Error: No valid response received", fg="red")

    except Exception as e:
        messagebox.showerror("API Error", f"Failed to get response: {e}")

# GUI Setup with Improved Design
root = tk.Tk()
root.title("AI Chatbot - Hugging Face")
root.geometry("600x500")
root.configure(bg="#F0F0F0")

# Load background image for answer box
bg_image = PhotoImage(file="images.png")  # Replace with your image file

#bg_image = PhotoImage(file="C:/Users/Amjith/Desktop/virtual_pa/images.jpg")  # Example path

# Heading
heading_label = tk.Label(root, text="Hugging Face Chatbot", font=("Helvetica", 18, "bold"), bg="#F0F0F0", fg="#333")
heading_label.pack(pady=10)

# Query Entry Box
query_entry = tk.Entry(root, width=50, font=("Helvetica", 14), bd=2, relief="solid")
query_entry.pack(pady=10)

# Generate Button
generate_button = tk.Button(root, text="Generate Response", command=generate_response, font=("Helvetica", 12, "bold"), 
                            bg="#4CAF50", fg="white", padx=20, pady=5, relief="raised", borderwidth=3)
generate_button.pack(pady=10)

# Answer Frame with Background Image
answer_frame = tk.Label(root, image=bg_image)
answer_frame.pack(pady=20)

# Answer Label (Placed Over Image)
answer_label = tk.Label(root, text="", font=("Helvetica", 14), fg="black", wraplength=500, justify="left", bg="#F0F0F0")
answer_label.place(x=100, y=200)  # Adjust position if needed

# Run Tkinter
root.mainloop()
'''

import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Import Pillow for image handling
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Adjust speech speed

def speak(text):
    """Function to convert text to speech."""
    engine.say(text)
    engine.runAndWait()

# Set your Hugging Face API key
HUGGINGFACE_API_KEY = "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"

# ✅ Use a working Hugging Face model
API_URL = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-alpha"

'''
def generate_response():
    """Fetch AI-generated response from Hugging Face API and display it with voice output."""
    user_input = query_entry.get().strip()

    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": user_input,
        "parameters": {"max_length": 50, "temperature": 0.7, "top_p": 0.9}
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response_data = response.json()

        # Handling potential errors in the response
        if response.status_code != 200:
            error_message = response_data.get("error", "Unknown error")
            answer_label.config(text=f"Error: {error_message}", fg="red")
            return

        # Extract generated text from response
        if isinstance(response_data, list) and len(response_data) > 0 and "generated_text" in response_data[0]:
            bot_reply = response_data[0]["generated_text"]
            answer_label.config(text=bot_reply, wraplength=400, justify="left", fg="white", bg="#000000")
            speak(bot_reply)  # Speak the generated response
        else:
            answer_label.config(text="Error: No valid response received", fg="red")

    except Exception as e:
        messagebox.showerror("API Error", f"Failed to get response: {e}")'''

import time

def generate_response():
    """Fetch AI-generated response from Hugging Face API and display it with voice output."""
    user_input = query_entry.get().strip()
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return

    headers = {
        "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": user_input,
        "parameters": {"max_length": 50, "temperature": 0.7, "top_p": 0.9}
    }

    retries = 3  # Number of retries
    for attempt in range(retries):
        try:
            response = requests.post(API_URL, headers=headers, json=data)
            print("Raw Response:", response.text)  # Debugging Step

            # If the model is busy, retry after a delay
            if response.status_code == 503:
                print("Model is busy, retrying in 5 seconds...")
                time.sleep(5)
                continue

            response_data = response.json()

            # Handle API errors
            if response.status_code != 200:
                error_message = response_data.get("error", "Unknown error")
                answer_label.config(text=f"Error: {error_message}", fg="red")
                return

            # Extract generated text from response
            if isinstance(response_data, list) and len(response_data) > 0 and "generated_text" in response_data[0]:
                bot_reply = response_data[0]["generated_text"]
                answer_label.config(text=bot_reply, wraplength=400, justify="left", fg="black")
                speak(bot_reply)
            else:
                answer_label.config(text="Error: No valid response received", fg="red")
            return

        except Exception as e:
            messagebox.showerror("API Error", f"Failed to get response: {e}")

    answer_label.config(text="Error: Model is unavailable. Try again later.", fg="red")


# GUI Setup with Background Image
root = tk.Tk()
root.title("AI Chatbot - Hugging Face")
root.geometry("600x500")

# Load the background image
bg_image = Image.open(r"C:\Users\Amjith\Desktop\images.png")  # Make sure this file is in the same folder
bg_image = bg_image.resize((600, 500))  # Resize image to match window size
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a Label widget to display the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Make it cover the full window

# Heading (Over Background)
heading_label = tk.Label(root, text="Hugging Face Chatbot", font=("Helvetica", 18, "bold"), fg="white", bg="#222")
heading_label.pack(pady=10)

# Query Entry Box
query_entry = tk.Entry(root, width=50, font=("Helvetica", 14), bd=2, relief="solid")
query_entry.pack(pady=10)

# Generate Button
generate_button = tk.Button(root, text="Generate Response", command=generate_response, font=("Helvetica", 12, "bold"), 
                            bg="#4CAF50", fg="white", padx=20, pady=5, relief="raised", borderwidth=3)
generate_button.pack(pady=10)

# Answer Label (Now Transparent Over Image)
answer_label = tk.Label(root, text="", font=("Helvetica", 14), wraplength=500, justify="left", fg="white", bg="#222")
answer_label.pack(pady=20)

# Run Tkinter
root.mainloop()


