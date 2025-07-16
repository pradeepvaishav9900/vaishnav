# Voice Assistant - Vaishnav ji (Groq + Whisper + Streamlit WebRTC)

import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, ClientSettings
import av
import requests
import tempfile
import base64
from datetime import datetime

# Set your Groq API key
GROQ_API_KEY = "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"  # 🔁 Replace with your actual Groq key
GROQ_HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Helper function to display response
def speak(text):
    st.write("🗣️ Vaishnav ji:", text)

# Whisper STT via Groq (mocked)
def whisper_transcribe(audio_path):
    # In real case, you'd use Whisper model here. For now, this is a placeholder.
    return "what is your name"

# Groq LLM call
def groq_chat(message):
    url = "https://api.groq.com/openai/v1/chat/completions"
    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are Vaishnav ji, a helpful Hindi voice assistant."},
            {"role": "user", "content": message}
        ]
    }
    response = requests.post(url, headers=GROQ_HEADERS, json=payload)
    return response.json()['choices'][0]['message']['content']

# WebRTC audio processor
class AudioProcessor(AudioProcessorBase):
    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            f.write(frame.to_ndarray().tobytes())
            audio_path = f.name

        # Transcribe with Whisper
        user_text = whisper_transcribe(audio_path)
        st.write("🧑 You:", user_text)

        # Response
        if "your name" in user_text:
            speak("My name is Vaishnav ji, your personal assistant!")

        elif "time" in user_text:
            time_now = datetime.now().strftime("%I:%M %p")
            speak(f"Current time is {time_now}")

        elif "how are you" in user_text:
            speak("I'm doing great! How can I help you?")

        elif "joke" in user_text:
            speak("Why did the computer go to the doctor? Because it had a virus!")

        else:
            reply = groq_chat(user_text)
            speak(reply)

        return frame

# UI
st.title("🧠 Voice Assistant - Vaishnav ji (Groq Version)")
st.write("Speak something and let Vaishnav ji help you!")

webrtc_streamer(
    key="voice",
    mode="sendonly",
    audio_processor_factory=AudioProcessor,
    client_settings=ClientSettings(media_stream_constraints={"video": False, "audio": True})
)

st.info("Allow microphone access to talk with Vaishnav ji")
