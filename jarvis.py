import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def speak(audio):
 engine.say(audio)
 engine.runAndWait()
def wishme():
    hour=int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
       speak("Good Morning! I am Jarvis. Please tell me how may I help you Sir")
      
    elif hour>=12 and hour<18:
       speak("Good Afternoon! I am Jarvis. Please tell me how may I help you Sir")
      
    elif hour>=18 and hour<24:
       speak("Good Evening I am Jarvis. Please tell me how may I help you Sir") 

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in') 
        print(f"User said: {query}\n")

    except Exception as e:
          
        print("Say that again please...")   
        return "None" 
    return query
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login("vaibhavbhadri@gmail.com", "your_password")
    server.sendmail("vaibhavbhadri@gmail.com", to, content)
    server.close()
if __name__ == "__main__":
    
    wishme()
    while True:
     
        query = takeCommand().lower() 

        if 'exit' in query or 'stop' in query or 'bye' in query or 'no' in query:
            speak("Goodbye Sir! Have a great day!")
            break

        if 'wikipedia' in query:  
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=6)
            speak("According to Wikipedia")
            print(results)
            speak(results)
            speak("Is there anything else you would like to know Sir?")
        elif 'open youtube' in query:
            speak("Opening Youtube....")
            webbrowser.open("youtube.com")
        elif 'open amazon' in query:
            speak("Opening Amazon....")
            webbrowser.open("amazon.in")
        elif 'open chatgpt' in query:
            speak("Opening ChatGPT....")
            webbrowser.open("chatgpt.com")
        elif 'play music' in query:
            speak("Playing the music Sir!")
            music = 'D:\\music_demo'
            songs = os.listdir(music)
            print(songs)
            os.startfile(os.path.join(music, songs[0]))
        elif 'the time' in query:
            time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, The Time is {time}")
            speak("Is there anything else you would like to know Sir?")
        elif 'open code' in query:
            path = "C:\\Users\\Admin\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            speak("Opening Visual Studio Code....")
            os.startfile(path)
        elif 'send email' in query:
            try:
                speak("What should I say Sir?")
                content = takeCommand()
                to = "vaibhavbhadri48@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent successfully Sir!")
            except Exception as e:
                print(e)
                speak("Sorry Sir! I am not able to send this email for you.")
