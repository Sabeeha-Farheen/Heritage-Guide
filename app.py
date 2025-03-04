import streamlit as st
import speech_recognition as sr
import io
from src.helper import llm_model_object, text_to_speech

# Set up page
st.set_page_config(page_title="Tamil Nadu Heritage Explorer", page_icon="🏛️", layout="wide")

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
    padding: 8px 16px;
    transition: 0.3s;
}
.stButton>button:hover {
    background-color: #1F2C3C;
    transform: scale(1.05);
}
.stTextArea textarea {
    border-radius: 8px;
    border: 1px solid #d1d5db;
}
.site-card {
    text-align: center;
    padding: 10px;
    border-radius: 8px;
    background: #f7f9fc;
    box-shadow: 0px 2px 6px rgba(0, 0, 0, 0.05);
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
        {"name": "Great Living Chola Temples", "image": "https://upload.wikimedia.org/wikipedia/commons/7/7b/Brihadisvara_Temple%2C_Thanjavur.jpg"},
        {"name": "Gangaikonda Cholapuram Temple", "image": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Gangaikonda_Cholapuram_Temple.jpg"},
        {"name": "Airavatesvara Temple", "image": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Airavatesvara_Temple_Darasuram.jpg"}
    ]
    
    st.markdown("### UNESCO World Heritage Sites in Tamil Nadu")
    cols = st.columns(3)
    for i, site in enumerate(sites):
        with cols[i]:
            st.image(site["image"], use_column_width=True)
            st.markdown(f"<div class='site-card'><b>{site['name']}</b></div>", unsafe_allow_html=True)

def main():
    st.title("🏛️ Tamil Nadu Heritage Guide")
    st.subheader("Discover Tamil Nadu's UNESCO Wonders")
    
    st.markdown("### Ask About Tamil Nadu's Heritage")
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("🎤 Tap to Speak"):
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
    
    display_unesco_sites()

if __name__ == '__main__':
    main()
