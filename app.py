import streamlit as st
import speech_recognition as sr
from src.helper import llm_model_object, text_to_speech  # Removed voice_input()

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
    st.title("Multilingual AI Assistant 🤖")

    if st.button("Ask me anything"):
        with st.spinner("Listening..."):
            text = voice_input()
            response = llm_model_object(text)
            text_to_speech(response)

            audio_file = open("speech.mp3", "rb")
            audio_bytes = audio_file.read()

            st.text_area(label="Response:", value=response, height=350)
            st.audio(audio_bytes)
            st.download_button(label="Download Speech",
                               data=audio_bytes,
                               file_name="speech.mp3",
                               mime="audio/mp3")

if __name__ == '__main__':
    main()
