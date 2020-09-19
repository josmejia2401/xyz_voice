
import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
#from mpyg321.mpyg321 import MPyg321Player
from playsound import playsound

def respond(audioString):
    print(audioString)
    #tts = gTTS(text=audioString, lang='en')
    tts = gTTS(text=audioString, lang='es-us')
    tts.save("speech.mp3")
    #player = MPyg321Player()
    #player.play_song("speech.mp3")
    #os.system("mpg321 speech.mp3")
    playsound("speech.mp3")

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("I am listening...")
        audio = r.listen(source=source, timeout=5, phrase_time_limit=5)
    data = ""
    try:
        data = r.recognize_google(audio)
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition did not understand audio")
    except sr.RequestError as e:
        print("Request Failed; {0}".format(e))
    return data

def digital_assistant(data):
    if "how are you" in data:
        respond("I am well")

    if "what time is it" in data:
        respond(ctime())
        
    if "apagar" in data:
        respond("Hasta la próxima")
        raise Exception("apagar")

    respond("Función invalida. En este momento no puedo de responder.")
    


time.sleep(2)
respond("Hola, cómo estás?")
while 1:
    data = listen()
    print(data)
    try:
        digital_assistant(data)
    except Exception as e:
        break
    
