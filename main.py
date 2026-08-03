"""
Voice Assistant AI
-------------------
A simple voice assistant that:
- Listens to your commands through the microphone (Speech to Text)
- Replies back with a natural voice (Text to Speech)
- Opens websites, tells the time, searches Wikipedia, and responds to greetings

Runs on Python 3.13.5
"""

import datetime
import webbrowser
import wikipedia
import speech_recognition as sr
from gtts import gTTS
import pygame
import tempfile
import os
import sys

# ============ Settings ============
LANGUAGE = "en"
ASSISTANT_NAME = "Your Assistant"

recognizer = sr.Recognizer()
pygame.mixer.init()


# ============ Speak (Text to Speech) ============
def speak(text: str):
    """Prints the text and plays it out loud"""
    print(f"🤖 {ASSISTANT_NAME}: {text}")
    try:
        tts = gTTS(text=text, lang=LANGUAGE)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name
        tts.save(temp_path)

        pygame.mixer.music.load(temp_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove(temp_path)
    except Exception as e:
        print(f"(Could not play audio: {e})")


# ============ Listen (Speech to Text) ============
def listen() -> str:
    """Listens through the microphone and converts speech to text"""
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=6, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio, language="en-US")
        print(f"🗣️ You: {text}")
        return text.lower()
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        speak("Could not reach the speech recognition service. Check your internet.")
        return ""
    except Exception:
        speak("Network connection timed out. Please check your internet and try again.")
        return ""


# ============ Handle Commands ============
def handle_command(command: str) -> bool:
    """
    Executes the requested command. Returns False if the user asked to exit.
    """
    if not command:
        return True

    if any(w in command for w in ["hello", "hi", "hey"]):
        speak("Hello! How can I help you?")

    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {now}")

    elif "date" in command or "today" in command:
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {today}")

    elif "youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")

    elif "google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")

    elif "wikipedia" in command:
        speak("What topic do you want to search for?")
        topic = listen()
        if topic:
            try:
                wikipedia.set_lang("en")
                summary = wikipedia.summary(topic, sentences=2)
                speak(summary)
            except Exception:
                speak("I couldn't find a clear result for that topic.")

    elif "who are you" in command:
        speak("I'm your smart voice assistant, ready to help anytime!")

    elif any(w in command for w in ["goodbye", "bye", "exit"]):
        speak("Goodbye!")
        return False

    else:
        speak("I didn't understand that, can you repeat it?")

    return True


# ============ Entry Point ============
def main():
    speak("Hello! I'm ready to listen. Say 'goodbye' to exit.")

    running = True
    while running:
        try:
            command = listen()
            running = handle_command(command)
        except KeyboardInterrupt:
            print("\nStopped manually.")
            sys.exit(0)


if __name__ == "__main__":
    main()