import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import random
import requests # <--  API requests ke liye
import json     # <--  parsing API responses ke liye
import threading# <-- timer feature   ke liye
import time as pytime # <--  timer feature ke liye

# --- Initialization ---

#  text-to-speech (TTS) engine initialization karne ke liye
try:
    engine = pyttsx3.init()
except ImportError:
    print("pyttsx3 not found. Please install it using: pip install pyttsx3")
    exit()
except RuntimeError:
    print("Failed to initialize pyttsx3. Make sure you have a working text-to-speech engine on your system.")
    exit()


# Initialize speech recognizer initialization ke liye
recognizer = sr.Recognizer()

# --- Core Functions ---

def speak(text):
    """
    This function takes text as input and uses the TTS engine to speak it out loud.
    """
    print(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """
    This function listens for user input from the microphone,
    recognizes the speech, and returns it as text.
    """
    with sr.Microphone() as source:
        print("\nListening for a command...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            print("Listening timed out.")
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            speak("Sorry, my speech service is currently down.")
            return ""
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return ""

def get_weather(city):
    """Fetches weather data for a given city using an API."""
    # Note: This uses a free API. No API key required for this specific endpoint.
    api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid=YOUR_API_KEY&units=metric"
    # For now, this will not work without an API key. 
    # Let's use a dummy response for demonstration.
    
    # --- Start of Dummy Data ---
    if city:
        speak(f"I'm sorry, I can't fetch live weather data without an API key. You can get a free one from openweathermap.org.")
        return
    # --- End of Dummy Data ---



def set_timer(duration_in_seconds):
    """Sets a timer for a given duration and announces when time is up."""
    def timer_expired():
        speak("Time's up!")
    
    speak(f"Timer set for {duration_in_seconds} seconds.")
    timer = threading.Timer(duration_in_seconds, timer_expired)
    timer.start()

def get_definition(word):
    """Fetches the definition of a word using a free dictionary API."""
    try:
        response = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}")
        data = response.json()
        if response.status_code == 200:
            definition = data[0]['meanings'][0]['definitions'][0]['definition']
            speak(f"The definition of {word} is: {definition}")
        else:
            speak(f"Sorry, I could not find the definition for {word}.")
    except Exception as e:
        print(e)
        speak("Sorry, I'm having trouble fetching the definition right now.")


def process_command(command):
    """
    This function takes the recognized command and performs an action based on keywords.
    """
    if not command:
        return True # Continue running

    # --- Predefined Commands ---
    if "hello" in command or "hi" in command:
        speak("Hello there! How can I assist you today?")
    
    elif "who are you" in command:
        speak("I am a voice assistant created in Python, here to help you with your tasks.")
        
    elif "help" in command or "what can you do" in command: # <-- NEW COMMAND
        speak("""
        You can ask me to:
        Tell the time or date.
        Get the weather in a city.
        Define a word.
        Set a timer.
        Search for something on Google.
        Open a website.
        Tell a joke.
        Open Notepad or Calculator.
        Restart or shut down your computer.
        Or say 'exit' to close me.
        """)

    elif "time" in command:
        now = datetime.datetime.now()
        current_time = now.strftime("%I:%M %p")
        speak(f"The current time is {current_time}.")

    elif "date" in command:
        today = datetime.datetime.now()
        current_date = today.strftime("%A, %B %d, %Y")
        speak(f"Today's date is {current_date}.")

    elif "weather in" in command:
        city = command.split("weather in ")[-1]
        get_weather(city)

    elif "define" in command:
        word = command.split("define ")[-1]
        get_definition(word)

    elif "set a timer for" in command:
        # Example: "set a timer for 10 seconds"
        try:
            parts = command.split()
            duration = int(parts[4])
            set_timer(duration)
        except (ValueError, IndexError):
            speak("Please specify a valid duration in seconds. For example, say 'set a timer for 10 seconds'.")

    elif "search for" in command:
        search_query = command.replace("search for", "").strip()
        if search_query:
            url = f"https://www.google.com/search?q={search_query}"
            speak(f"Searching Google for {search_query}.")
            webbrowser.open(url)
        else:
            speak("What would you like me to search for?")

    elif "open" in command and ".com" in command:
        website = command.replace("open", "").strip()
        speak(f"Opening {website}.")
        webbrowser.open(f"http://{website}")

    elif "joke" in command:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
        ]
        speak(random.choice(jokes))
    
    elif "open notepad" in command:
        speak("Opening Notepad.")
        os.system("start notepad.exe")

    elif "open calculator" in command:
        speak("Opening Calculator.")
        os.system("start calc.exe")
        
    elif "shutdown" in command:
        speak("Are you sure you want to shut down? Say yes to confirm.")
        confirmation = listen_for_command()
        if "yes" in confirmation:
            speak("Shutting down.")
            os.system("shutdown /s /t 1")
            return False
        else:
            speak("Shutdown cancelled.")
            
    elif "restart" in command:
        speak("Are you sure you want to restart? Say yes to confirm.")
        confirmation = listen_for_command()
        if "yes" in confirmation:
            speak("Restarting.")
            os.system("shutdown /r /t 1")
            return False
        else:
            speak("Restart cancelled.")

    elif "exit" in command or "goodbye" in command or "stop" in command:
        speak("Goodbye! Have a great day.")
        return False

    else:
        speak("I'm not sure how to help with that. You can ask me the time, date, weather, or to define a word.")

    return True

# --- Main Loop ---
if __name__ == "__main__":
    speak("Voice assistant activated. How can I help you?")
    running = True
    while running:
        command = listen_for_command()
        running = process_command(command)