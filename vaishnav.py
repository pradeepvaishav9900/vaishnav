import streamlit as st
import requests
import tempfile
import os
from datetime import datetime
from io import BytesIO
import base64

# Set your Groq API key
GROQ_API_KEY = "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"  # 🔁 Replace with your actual Groq key
GROQ_HEADERS = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

# Helper function to display response
def speak(text):
    st.write("🗣️ Vaishnav ji:", text)

# Upload audio and transcribe using Whisper
def whisper_transcribe(file):
    files = {"file": ("audio.wav", file, "audio/wav")}
    response = requests.post(
        "https://api.groq.com/openai/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        files=files,
        data={"model": "whisper-large-v3"}
    )
    return response.json().get("text", "")

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

# UI
st.title("🎤 Voice Assistant - Vaishnav ji (Groq Version)")
st.write("Record or upload your voice. Vaishnav ji will reply!")

# Voice uploader
audio_file = st.file_uploader("Upload a .wav audio file", type=["wav"])

if audio_file is not None:
    st.audio(audio_file, format="audio/wav")
    with st.spinner("Transcribing with Whisper..."):
        user_text = whisper_transcribe(audio_file)
        st.write("🧑 You:", user_text)

        # Static responses
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

else:
    st.info("Please upload a WAV audio file to begin.")
