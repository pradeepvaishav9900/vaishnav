# Voice Assistant - Vaishnav ji (Streamlit Cloud Compatible)

import streamlit as st
from streamlit_audio_recorder import audio_recorder
import openai
import base64
import requests
import tempfile

# Set your OpenAI API key
# openai.api_key = "your-api-key-here"

# Helper function to speak (text-to-speech)
def speak(text):
    st.write("🗣️ Vaishnav ji:", text)

# Streamlit UI
st.title("🧠 Voice Assistant - Vaishnav ji")
st.write("Speak something and let Vaishnav ji help you!")

# Record Audio
wav_audio_data = audio_recorder(text="🎙️ Click to record your voice", pause_threshold=2.0, sample_rate=44100)

if wav_audio_data:
    st.audio(wav_audio_data, format='audio/wav')

    # Save audio to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(wav_audio_data)
        tmp_filename = tmp_file.name

    # Send audio to Whisper (speech-to-text)
    with open(tmp_filename, "rb") as f:
        transcript = openai.Audio.transcribe("whisper-1", f)
        command = transcript["text"]
        st.write("🧑 You:", command)

    # Logic based on command
    if "your name" in command:
        speak("My name is Vaishnav ji, your personal assistant!")

    elif "time" in command:
        from datetime import datetime
        time_now = datetime.now().strftime("%I:%M %p")
        speak(f"Current time is {time_now}")

    elif "how are you" in command:
        speak("I'm doing great! How can I help you?")

    elif "joke" in command:
        speak("Why did the computer go to the doctor? Because it had a virus!")

    else:
        # Use OpenAI API to get response
        # response = openai.ChatCompletion.create(
        #     model="gpt-3.5-turbo",
        #     messages=[{"role": "user", "content": command}]
        # )
        # reply = response['choices'][0]['message']['content']
        reply = "This is a dummy response. Connect your OpenAI key to get real replies."
        speak(reply)

else:
    st.info("Click the button to record your question.")
