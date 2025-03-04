import streamlit as st
import speech_recognition as sr
import io

# Increase page width and set background
st.set_page_config(
    page_title="Tamil Nadu Heritage Explorer", 
    page_icon="🏛️", 
    layout="wide"
)

# Comprehensive CSS for improved design
st.markdown("""
<style>
.main {
    background-color: white;
    font-family: 'Inter', 'Helvetica Neue', sans-serif;
}
.stApp {
    max-width: 1200px;
    margin: 0 auto;
    padding: 30px;
    background-color: white;
}
.stButton>button {
    background-color: #2C3E50;
    color: white !important;
    border: none;
    border-radius: 20px;
    padding: 10px 20px;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    background-color: #34495E;
    transform: scale(1.05);
}
.stTextArea>div>div>textarea {
    background-color: #F7F9FC;
    border-radius: 10px;
    border: 1px solid #E0E4E8;
    color: black !important;
}
.stAlert {
    border-radius: 10px;
}
h1, h3, p, div, span {
    color: black !important;
}
.unesco-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 20px;
    margin-top: 30px;
}
.unesco-card {
    border: 1px solid #E0E4E8;
    border-radius: 10px;
    overflow: hidden;
    transition: transform 0.3s ease;
}
.unesco-card:hover {
    transform: scale(1.05);
}
.unesco-card img {
    width: 100%;
    height: 250px;
    object-fit: cover;
}
.unesco-card .site-name {
    padding: 10px;
    text-align: center;
    background-color: #F7F9FC;
}
</style>
""", unsafe_allow_html=True)

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

def display_unesco_sites():
    # UNESCO sites in Tamil Nadu
    unesco_sites = [
        {
            "name": "Great Living Chola Temples",
            "image": "https://upload.wikimedia.org/wikipedia/commons/7/7b/Brihadisvara_Temple%2C_Thanjavur.jpg"
        },
        {
            "name": "Gangaikonda Cholapuram Temple",
            "image": "https://upload.wikimedia.org/wikipedia/commons/2/2d/Gangaikonda_Cholapuram_Temple.jpg"
        },
        {
            "name": "Airavatesvara Temple",
            "image": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Airavatesvara_Temple_Darasuram.jpg"
        }
    ]

    st.markdown("### UNESCO World Heritage Sites in Tamil Nadu")
    
    # Create a grid of UNESCO sites
    site_html = "<div class='unesco-grid'>"
    for site in unesco_sites:
        site_html += f"""
        <div class='unesco-card'>
            <img src='{site["image"]}' alt='{site["name"]}'>
            <div class='site-name'>{site["name"]}</div>
        </div>
        """
    site_html += "</div>"
    
    st.markdown(site_html, unsafe_allow_html=True)

def main():
    # Main content
    st.markdown("<h1>🏛️ Tamil Nadu Heritage Guide</h1>", unsafe_allow_html=True)
    st.markdown("<h3>Discover UNESCO Wonders Through AI</h3>", unsafe_allow_html=True)

    # Voice input section
    st.markdown("### Ask About Tamil Nadu's Heritage")
    
    # Create a centered container for the voice input button
    col1, col2, col3 = st.columns([1,2,1])
    
    with col2:
        voice_button = st.button("🎤 Tap to Speak", key="voice_input")
    
    text = ""
    if voice_button:
        with st.spinner("Listening..."):
            text = voice_input()
            st.success(f"You said: **{text}**")

    # Response generation
    if text and text not in ["Sorry, I couldn't understand the audio.", "Error connecting to speech recognition service."]:
        with st.spinner("Exploring Heritage..."):
            try:
                # Generate response
                response = llm_model_object(text)
                
                # Text to speech
                text_to_speech(response)

                # Read audio file
                with open("speech.mp3", "rb") as audio_file:
                    audio_bytes = io.BytesIO(audio_file.read())

                # Display response with card-like styling
                st.markdown("### AI Heritage Guide Response")
                st.markdown(f"""
                <div style='
                    background-color: #F7F9FC; 
                    border-radius: 10px; 
                    padding: 20px; 
                    border: 1px solid #E0E4E8;
                    color: black;
                '>
                {response}
                </div>
                """, unsafe_allow_html=True)

                # Audio controls
                col1, col2, col3 = st.columns([1,1,1])
                
                with col2:
                    st.audio(audio_bytes, format="audio/mp3")
                
                with col3:
                    st.download_button(
                        "Download Audio", 
                        data=audio_bytes, 
                        file_name="heritage_guide.mp3", 
                        mime="audio/mp3",
                        key="download_audio"
                    )

            except Exception as e:
                st.error(f"Error exploring heritage: {str(e)}")

    # Display UNESCO sites grid
    display_unesco_sites()

if __name__ == '__main__':
    main()