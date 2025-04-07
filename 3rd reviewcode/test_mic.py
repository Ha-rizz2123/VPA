import speech_recognition as sr

def test_microphone():
    r = sr.Recognizer()
    
    # 🔹 Get available microphones
    print("🔍 Available Microphones:")
    for i, mic in enumerate(sr.Microphone.list_microphone_names()):
        print(f"{i}: {mic}")

    mic_index = int(input("\n🎤 Enter the microphone index to use: "))

    with sr.Microphone(device_index=mic_index) as source:
        print("🎤 Say something... (Speak clearly)")
        r.adjust_for_ambient_noise(source, duration=2)  
        audio = r.listen(source, timeout=10, phrase_time_limit=10)  

    try:
        print("✅ Processing...")
        text = r.recognize_google(audio, language="en-IN")
        print(f"🗣️ Recognized: {text}")
    except sr.UnknownValueError:
        print("❌ Could not understand audio. Please repeat.")
    except sr.RequestError:
        print("❌ Error connecting to Google Speech API.")

if __name__ == "__main__":
    test_microphone()
