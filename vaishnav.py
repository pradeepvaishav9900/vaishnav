# Voice Assistant using Streamlit + Speech Recognition + Text-to-Speech

import streamlit as st
import speech_recognition as sr
import pyttsx3
import openai

# Set your OpenAI API key if using online model
# openai.api_key = 'your-api-key-here'

# Initialize TTS engine
engine = pyttsx3.init()
def speak(text):
    st.write("🗣️ Vaishnav ji:", text)
    engine.say(text)
    engine.runAndWait()

# Streamlit UI
st.title("🧠 Voice Assistant - Vaishnav ji")
st.write("Speak something and let Vaishnav ji help you!")

if st.button("🎙️ Start Listening"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio, language='en-IN')
        st.write("🧑 You:", command)

        # Offline logic (add custom commands below)
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

        # If using online AI model
        else:
            # Use this block only if OpenAI/Groq key is set
            # response = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     messages=[{"role": "user", "content": command}]
            # )
            # reply = response['choices'][0]['message']['content']
            reply = "This is a dummy response. You can connect it to ChatGPT if API is set."
            speak(reply)

    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please speak clearly.")

    except sr.RequestError as e:
        speak("Could not request results; check your internet connection.")
