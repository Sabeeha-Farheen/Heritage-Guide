import streamlit as st
import speech_recognition as sr
import io
import os
from PIL import Image
from src.helper import llm_model_object, text_to_speech

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand the audio."
    except sr.RequestError:
        return "Error connecting to speech recognition service."

def main():
    # Travel-themed UI
    st.set_page_config(page_title="Travel AI Assistant", layout="wide")
    st.title("✈️ Explore the World with AI")
    st.markdown("### Your personal multilingual travel guide!")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("mic_icon.png", width=100)
        if st.button("🎤 Speak Now"):
            with st.spinner("Listening..."):
                text = voice_input()
                st.success(f"You said: **{text}**")
    
    if text and text not in ["Sorry, I couldn't understand the audio.", "Error connecting to speech recognition service."]:
        with st.spinner("Generating response..."):
            try:
                response = llm_model_object(text)
                text_to_speech(response)
                
                with open("speech.mp3", "rb") as audio_file:
                    audio_bytes = io.BytesIO(audio_file.read())
                
                st.text_area("🌍 AI Guide Says:", value=response, height=250)
                st.audio(audio_bytes)
                st.download_button("📥 Download Speech", data=audio_bytes, file_name="speech.mp3", mime="audio/mp3")
            except Exception as e:
                st.error(f"Error processing response: {str(e)}")
    
    with col2:
        st.image("travel_map.jpg", use_column_width=True)
        st.markdown("##### Discover landmarks, learn about cultures, and explore destinations like never before!")

if __name__ == '__main__':
    main()
