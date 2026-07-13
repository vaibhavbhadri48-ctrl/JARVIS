import asyncio
import tempfile
import edge_tts
import pygame
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib

pygame.mixer.init()
_SPEECH_FILE = os.path.join(tempfile.gettempdir(), "jarvis_speech.mp3")

async def _generate_speech(text, filename):
    communicate = edge_tts.Communicate(text, voice="en-US-GuyNeural")
    await communicate.save(filename)

def speak(text):
    print(f"JARVIS: {text}")
    try:
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
    except Exception:
        pass
    asyncio.run(_generate_speech(text, _SPEECH_FILE))
    pygame.mixer.music.load(_SPEECH_FILE)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def wishme():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning! I am Jarvis. Please tell me how may I help you Sir")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon! I am Jarvis. Please tell me how may I help you Sir")
    else:
        speak("Good Evening! I am Jarvis. Please tell me how may I help you Sir")

def takeCommand():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 1
            r.adjust_for_ambient_noise(source, duration=0.5)
            audio = r.listen(source, timeout=6, phrase_time_limit=8)

        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
        return query.lower()

    except sr.WaitTimeoutError:
        print("Listening timed out, no speech detected.")
        return "none"
    except sr.UnknownValueError:
        print("Say that again please...")
        return "none"
    except sr.RequestError:
        print("Speech service is unreachable. Check your internet connection.")
        return "none"
    except Exception as e:
        print(f"Microphone/listening error: {e}")
        return "none"

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("vaibhavbhadri@gmail.com", "your_app_password")
    server.sendmail("vaibhavbhadri@gmail.com", to, content)
    server.close()

if __name__ == "__main__":
    wishme()

    while True:
        query = takeCommand()

        if query == "none":
            continue

        try:
            if 'exit' in query or 'stop' in query or 'bye' in query:
                speak("Goodbye Sir! Have a great day!")
                break

            elif 'wikipedia' in query:
                speak('Searching Wikipedia...')
                topic = query.replace("wikipedia", "").strip()
                try:
                    results = wikipedia.summary(topic, sentences=2)
                    speak("According to Wikipedia")
                    print(results)
                    speak(results)
                except wikipedia.exceptions.DisambiguationError:
                    speak("That topic is ambiguous. Could you be more specific?")
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I could not find anything on that topic.")
                speak("Is there anything else you would like to know Sir?")

            elif 'open youtube' in query:
                speak("Opening Youtube....")
                webbrowser.open("https://youtube.com")

            elif 'open amazon' in query:
                speak("Opening Amazon....")
                webbrowser.open("https://amazon.in")

            elif 'open erp' in query:
                speak("Opening ERP....")
                webbrowser.open("https://erp.geu.ac.in/")

            elif 'play music' in query:
                music_dir = 'D:\\music_demo'
                if os.path.isdir(music_dir) and os.listdir(music_dir):
                    songs = os.listdir(music_dir)
                    speak("Playing the music Sir!")
                    os.startfile(os.path.join(music_dir, songs[0]))
                else:
                    speak("I could not find any music in the configured folder.")

            elif 'the time' in query:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                speak(f"Sir, the time is {current_time}")
                speak("Is there anything else you would like to know Sir?")

            elif 'open code' in query:
                path = "C:\\Users\\dell\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
                if os.path.exists(path):
                    speak("Opening Visual Studio Code....")
                    os.startfile(path)
                else:
                    speak("I could not find Visual Studio Code at the configured path.")

            elif 'send email' in query:
                speak("What should I say Sir?")
                content = takeCommand()
                if content == "none":
                    speak("I did not catch that, cancelling the email.")
                else:
                    to = "vaibhavbhadri48@gmail.com"
                    sendEmail(to, content)
                    speak("Email has been sent successfully Sir!")

            else:
                speak("Sorry, I did not understand that command.")

        except Exception as e:
            print(f"An error occurred while executing the command: {e}")
            speak("Sorry Sir, something went wrong with that. Please try again.")