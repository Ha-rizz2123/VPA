import tkinter as tk
from tkinter import messagebox
import pyttsx3

# Initialize text-to-speech
engine = pyttsx3.init()
engine.setProperty('rate', 150)

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def generate_response():
    """Generate a simple response to the user's query."""
    user_input = query_entry.get().strip()
    
    if not user_input:
        messagebox.showwarning("Input Error", "Please enter a prompt.")
        return
    
    # Simple response generation (no API calls)
    responses = {
        "hello": "Hello! How can I help you today?",
        "how are you": "I'm just a simple program, but I'm functioning well. How are you?",
        "what time is it": "I don't have access to your system clock. Please check your device.",
        "tell me a joke": "Why don't scientists trust atoms? Because they make up everything!",
        "who are you": "I'm a simple chatbot created for demonstration purposes.",
        "thank you": "You're welcome! Is there anything else I can help with?",
        "bye": "Goodbye! Have a great day!"
    }
    
    # Find the closest match or use default response
    response = "I'm a simple demo chatbot. In the full version, I would connect to an AI service."
    for key in responses:
        if key in user_input.lower():
            response = responses[key]
            break
    
    # Display and speak the response
    answer_label.config(text=response)
    speak(response)

# Create main window
root = tk.Tk()
root.title("Simple ChatGPT Demo")
root.geometry("500x400")
root.configure(bg="#f0f0f0")

# Create a frame for better organization
main_frame = tk.Frame(root, bg="#f0f0f0", padx=20, pady=20)
main_frame.pack(fill="both", expand=True)

# Header
header_label = tk.Label(main_frame, text="ChatGPT Demo", font=("Arial", 18, "bold"), bg="#f0f0f0")
header_label.pack(pady=(0, 20))

# Instructions
instructions_label = tk.Label(main_frame, 
                             text="Enter your question below. Try saying hello, asking how I am, or requesting a joke.",
                             font=("Arial", 10), bg="#f0f0f0", wraplength=400)
instructions_label.pack(pady=(0, 20))

# Query entry
query_entry = tk.Entry(main_frame, font=("Arial", 12), width=40)
query_entry.pack(pady=10)

# Generate button
generate_button = tk.Button(main_frame, text="Send", font=("Arial", 12, "bold"),
                           bg="#4CAF50", fg="white", padx=10, pady=5, command=generate_response)
generate_button.pack(pady=10)

# Answer frame
answer_frame = tk.Frame(main_frame, bg="#e0e0e0", padx=15, pady=15, bd=1, relief=tk.SOLID)
answer_frame.pack(fill="both", expand=True)

# Answer label
answer_label = tk.Label(answer_frame, text="Your responses will appear here", 
                       font=("Arial", 12), bg="#e0e0e0", wraplength=400, justify="left")
answer_label.pack(anchor="w")

# Initial message
speak("Welcome to the ChatGPT demo. Please type your question and press Send.")

# Start the GUI
root.mainloop()