import pyttsx3
import speech_recognition as SR
from googletrans import Translator
from gtts import gTTS 
import datetime 
import wikipedia 
import webbrowser
import os 
import smtplib
import sys
import requests, json
import time 

contacts = {"myself" : "email-here", "mom" : "email-here", "dad" : "email-here"} 
months = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June", 7:"July", 8:"August", 9:"September", 10:"October", 11:"November", 12:"December"}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# for voice in voices:
#     print(voice.id)
engine.setProperty('voice', voices[1].id)
# engine.say("I will speak this text")
# engine.runAndWait()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def greet_me():
    curr_hour = int(datetime.datetime.now().hour)
    if curr_hour >= 0 and curr_hour < 12:
        speak("Good Morning!")
    elif curr_hour >= 12 and curr_hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am Shezza, How may I help you?")

def obey_command():
    # It takes input from the microphone and returns output as a string
    mic = SR.Recognizer()
    with SR.Microphone() as source:
        print("Listening...")
        mic.pause_threshold = 1
        audio = mic.listen(source)
    
    try:
        print("Recognizing...")
        query = mic.recognize_google(audio, language='en-in')
        print(query)

    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query

def send_email(to, message):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your-email-here', 'your-password-here') 
    server.sendmail('your-email-here', to, 'Subject: Mailed via Shezza\n\n' + message)
    server.close()

def translate(query):
    translator = Translator()
    from_lang = 'en'
    to_lang = 'hi'

    try:
        text_to_translate = translator.translate(query, src = from_lang, dest = to_lang)
        text = text_to_translate.text
        say = gTTS(text = text, lang = to_lang, slow = False)
        say.save("captured_voice.mp3")      
        os.system("start captured_voice.mp3")
        # speak("What else can I do for you?")    

    except SR.UnknownValueError: 
        print("Unable to Understand the Input") 
              
    except SR.RequestError as e: 
        print("Unable to provide Required Output")
        format(e)

    except Exception as e:
        print(e)

def weather(city_name):
    api_key = "unique-API-key-here" #OpenWeather Unique Key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name
    response = requests.get(complete_url) 
    x = response.json() 
    
    if x["cod"] != "404": #x is a nested dictionary
        y = x["main"]   
        curr_temp = y["temp"] 
        curr_pressure = y["pressure"] 
        curr_humidity = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"] 
        speak(f"Temperature {curr_temp} Kelvin")
        speak(f"Pressure {curr_pressure} hectopascals")
        speak(f"Humidity {curr_humidity} percent")
        speak(f"Overall weather description {weather_description}")
        speak("What else can I do for you?")
    else:
        speak("Location not found!")

def alarm(alarm_time):
    while True:
        Standard_time=datetime.datetime.now().strftime("%H:%M")
        time.sleep(1)
        if alarm_time==Standard_time:
            count=0
            while count<=2:
                count=count+1
                speak("Wake up!")
            break
    
if __name__ == "__main__":
    # speak('Hello Anshika, let us get this done!')
    greet_me()
    
    while True:
        query = obey_command().lower()

        #To avoid opening URLs in microsoft's default web browser
        chrome_path = "C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s"

        #Logic for executing tasks based on query
        if 'wikipedia' in query:
            speak("Searching wikipedia")
            query = query.replace("wikipedia", "")
            result = wikipedia.summary(query, sentences=2)
            speak("According to wikipedia")
            speak(result)
            speak("What else can I do for you?")
        
        elif 'open vs code' in query:
            path = "C:\\Users\\yansh\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(path)
            speak("What else can I do for you?")

        elif 'open microsoft word' in query:
            path = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
            os.startfile(path)
            speak("What else can I do for you?")

        elif 'open' in query:
            query = query.replace('open', "")
            webbrowser.get(chrome_path).open(query)
            speak("What else can I do for you?")
        
        elif 'play music' in query:
            music_dir = 'D:\\Music'
            songs = os.listdir(music_dir)
            # print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))

        elif 'the time' in query:
            curr_time = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {curr_time}")
            speak("What else can I do for you?")

        elif 'the day' in query:
            curr_day = datetime.datetime.now().strftime("%A")
            speak(f"Today is {curr_day}")
            speak("What else can I do for you?")

        elif 'the date' in query:
            curr_date = datetime.datetime.today()
            speak(f"It's {curr_date.day, months[curr_date.month], curr_date.year} today")
            speak("What else can I do for you?")
        
        elif 'send email' in query:
            try:
                speak("What should it say?")
                message = obey_command()
                query = query.replace('send email to ', "")
                to = contacts[query]
                # to = "email-here"
                send_email(to, message)
                speak("Email has been sent successfully")
                speak("What else can I do for you?")
            except Exception as e:
                print(e)
                speak("Attempt unsuccessful")

        elif 'translate' in query:
            speak("What do you want to translate?")
            query = obey_command()
            translate(query)
        
        elif 'weather' in query:
            speak("Which city do you want to know the weather of?")
            city_name = obey_command()
            weather(city_name)

        elif 'alarm' in query:
            speak("Input the time you want to set the alarm for!")
            # alarm_time_hr = obey_command()
            # alarm_time_min = obey_command()
            # alarm_time = alarm_time_hr + ":" + alarm_time_min
            alarm_time = input("hh:mm -> ")
            alarm(alarm_time)

        elif 'thank you' in query:
            speak("Oh come on, it's my job!")

            # speak("What else can I do for you?")
        # terminating condition
        elif 'shutdown' in query:
            speak("Alright! Initiating shutdown in three, two, one... I'm off")
            sys.exit()
