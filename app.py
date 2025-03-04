import streamlit as st
import speech_recognition as sr
import io
from src.helper import llm_model_object, text_to_speech

# Set up page
st.set_page_config(page_title="Tamil Nadu Heritage Explorer", page_icon="🏩", layout="wide")

# Apply minimalistic CSS
st.markdown("""
<style>
body {
    font-family: 'Inter', sans-serif;
    background-color: #f8f9fa;
}
.stApp {
    max-width: 900px;
    margin: auto;
    padding: 20px;
    background: white;
    border-radius: 10px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
}
.stButton>button {
    background-color: #2C3E50;
    color: white;
    border-radius: 8px;
    padding: 12px 20px;
    transition: 0.3s;
    font-weight: bold;
}
.stButton>button:hover {
    background-color: #1F2C3C;
    transform: scale(1.05);
}
.center-button {
    display: flex;
    justify-content: center;
}
.site-card {
    text-align: center;
    padding: 10px;
    border-radius: 8px;
    background: #f7f9fc;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.05);
}
h1, h3, p, div, span {
    color: #2C3E50;
}
</style>
""", unsafe_allow_html=True)

def voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("Listening... Speak now!")
        audio = recognizer.listen(source)
    
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand."
    except sr.RequestError:
        return "Speech recognition service error."

def display_unesco_sites():
    sites = [
        {"name": "Great Living Chola Temples", "image": "C:/Users/Sabeeha Farheen/OneDrive/Desktop/img/chola tamples.jpeg"},
        {"name": "Gangaikonda Cholapuram Temple", "image": "C:/Users/Sabeeha Farheen/OneDrive/Desktop/img/gangaikonda-cholapuram.webp"},
        {"name": "Airavatesvara Temple", "image": "C:/Users/Sabeeha Farheen/OneDrive/Desktop/img/airavatesvara-temple.webp"}
    ]
    
    st.markdown("### UNESCO World Heritage Sites in Tamil Nadu")
    cols = st.columns(3)
    for i, site in enumerate(sites):
        with cols[i]:
            st.image(site["image"], width=250, use_container_width=False)
            st.markdown(f"<div class='site-card'><b>{site['name']}</b></div>", unsafe_allow_html=True)

def main():
    st.title("🏛️ Tamil Nadu Heritage Guide")
    st.subheader("Discover Tamil Nadu's UNESCO Wonders")
    
    st.markdown("### Ask About Tamil Nadu's Heritage")
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button("🎧 Tap to Speak"):
        with st.spinner("Listening..."):
            text = voice_input()
            st.success(f"You said: **{text}**")
            
            if text and "Sorry" not in text:
                with st.spinner("Exploring Heritage..."):
                    response = llm_model_object(text)
                    text_to_speech(response)
                    
                    with open("speech.mp3", "rb") as audio_file:
                        audio_bytes = io.BytesIO(audio_file.read())
                    
                    st.markdown("### AI Heritage Guide Response")
                    st.markdown(f"<div class='site-card' style='padding: 15px;'>{response}</div>", unsafe_allow_html=True)
                    st.audio(audio_bytes, format="audio/mp3")
                    st.download_button("Download Audio", data=audio_bytes, file_name="heritage_guide.mp3", mime="audio/mp3")
    st.markdown('</div>', unsafe_allow_html=True)
    
    display_unesco_sites()

if __name__ == '__main__':
    main()
