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
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand the audio.")
        return ""
    except sr.RequestError as e:
        print(f"Could not request result from Google Speech Recognition service: {e}")
        return ""

def text_to_speech(text):
    try:
        tts = gTTS(text=text, lang="en")
        tts.save("speech.mp3")  # Save speech to MP3
    except Exception as e:
        print(f"Error in text-to-speech conversion: {e}")

def llm_model_object(user_text):
    try:
        model = genai.GenerativeModel(model_name="gemini-1.5-flash")
        response = model.generate_content(user_text)
        return response.text if response else "No response received."
    except Exception as e:
        print(f"Error in generating response: {e}")
        return "An error occurred with the AI model."


    
    
    