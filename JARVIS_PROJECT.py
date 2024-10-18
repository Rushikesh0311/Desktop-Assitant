import speech_recognition as sr
import webbrowser
import pyttsx3
import MusicLibrary
import openai
import requests
from openai import openai_response

# Initialize recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi_key = "5c437edb6bdd4dfe98226f91b224439a"

# Function to speak a given text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to process OpenAI requests
def aiprocess(command):
    openai.api_key = "5c437edb6bdd4dfe98226f91b224439a"  # Use your OpenAI API key here
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a virtual assistant named Jarvis skilled in general tasks like Alexa and Google Cloud."},
                {"role": "user", "content": command}
            ]
        )
        return response.choices[0]['message']['content']
    except Exception as e:
        return f"Error with OpenAI API: {e}"

# Function to process voice commands for opening websites, playing music, or fetching news
def processCommand(command):
    command = command.lower()
    
    if "open google" in command:
        speak("Opening Google")
        webbrowser.open("https://google.com")
    
    elif "open youtube" in command:
        speak("Opening YouTube")
        webbrowser.open("https://youtube.com")
    
    elif "open facebook" in command:
        speak("Opening Facebook")
        webbrowser.open("https://facebook.com")
    
    elif "open linkedin" in command:
        speak("Opening LinkedIn")
        webbrowser.open("https://linkedin.com")
    
    elif "open whatsapp" in command:
        speak("Opening WhatsApp")
        webbrowser.open("https://whatsapp.com")
    
    elif command.startswith("play"):
        song = command.split(" ", 1)[1]
        if song in MusicLibrary.music:
            link = MusicLibrary.music[song]
            speak(f"Playing {song}")
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in the music library.")
    
    elif "news" in command.lower():
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi_key}")
            if r.status_code == 200:
                data = r.json()
                headlines = [article['title'] for article in data['articles']]
                for i, headline in enumerate(headlines, 1):
                    speak(f"{i}. {headline}")
            else:
                speak("Failed to retrieve news.")
        except Exception as e:
            speak(f"Error retrieving news: {e}")
    
    else:
        # Let OpenAI handle the request
        output = aiprocess(command)
        speak(output)

# Main program
if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    while True:
        try:
            # First listen for 'Jarvis' keyword
            with sr.Microphone() as source:
                print("Listening for 'Jarvis' keyword...")
                recognizer.adjust_for_ambient_noise(source)  # Reduce background noise
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=3)

            # Recognize keyword
            command = recognizer.recognize_google(audio)
            print(f"User said: {command}")

            if "jarvis" in command.lower():
                speak("How can I assist you?")

                # Listen for the next command after keyword 'Jarvis'
                with sr.Microphone() as source:
                    print("Listening for command...")
                    recognizer.adjust_for_ambient_noise(source)
                    audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)

                # Recognize and process the command
                new_command = recognizer.recognize_google(audio)
                print(f"Command: {new_command}")
                processCommand(new_command)

        # Handle errors
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that. Please try again.")
            print("UnknownValueError: Could not understand the audio.")
        
        except sr.RequestError as e:
            speak("There was an issue with the speech recognition service.")
            print(f"RequestError: {e}")
        
        except Exception as e:
            print(f"Unexpected error: {e}")
