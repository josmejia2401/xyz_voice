import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
from playsound import playsound

class XYZRespond(object):
    def __init__(self):
        super().__init__()
        

    def run(self, audioString):
        print(audioString)
        self.tts = gTTS(text=audioString, lang='es-us')
        self.tts.save("audio.mp3")
        playsound("audio.mp3")

class XYZListen(object):

    def __init__(self):
        super().__init__()

    def run(self):
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("I am listening...")
                audio = r.listen(source=source, timeout=5, phrase_time_limit=5)
            data = ""
            if audio:
                data = r.recognize_google(audio)
                print("listen: " + data)
            else:
                data = "no se pudo procesar la solicitud. Intenta nuevamente."
            return data
        except sr.UnknownValueError:
            print("Google Speech Recognition did not understand audio")
        except sr.RequestError as e:
            print("Request Failed; {0}".format(e))
        return "No escuche nada. Repite por favor."