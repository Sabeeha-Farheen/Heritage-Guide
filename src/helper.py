import speech_recognition as sr
import google.generativeai as genai
from dotenv import load_dotenv
import os
from gtts import gTTS

# Load environment variables
load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)  # ✅ Adjust for background noise
        print("Listening... Speak now!")
        audio = recognizer.listen(source, timeout=5)  # ✅ Add timeout for better response

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
        return "I couldn't understand. Please try again."
    except sr.RequestError as e:
        print(f"Error connecting to Google Speech Recognition: {e}")
        return "Speech recognition service error."


def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang="en")
        tts.save("speech.mp3")  # Save speech to MP3
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")

def llm_model_object(user_text):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")  # ✅ Using Flash model
        response = model.generate_content(user_text)
        return response.text if response else "No response received."
    except Exception as e:
        print(f"AI Model Error: {e}")  # ✅ Print exact error
        return f"AI Model Error: {e}"  # ✅ Return error for debugging



    
    
    