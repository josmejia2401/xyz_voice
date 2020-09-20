import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
from playsound import playsound

class XYZRespond(object):

    def __init__(self):
        super().__init__()
        self.OUTPUT_VAL = 0
    
    def get_name_output(self) -> str:
        self.OUTPUT_VAL += 1
        return "AUDIO_%d.mp3".format(self.OUTPUT_VAL)
    def run(self, audioString):
        print(audioString)
        self.tts = gTTS(text=audioString, lang='es-ES')
        name = self.get_name_output()
        self.tts.save(name)
        playsound(name)

class XYZListen(object):

    def __init__(self):
        super().__init__()
        self.r_main = sr.Recognizer()
        self.r_main.energy_threshold = 4000
        self.r_main.pause_threshold = 0.8

        self.r_keyword = sr.Recognizer()
        self.r_keyword.energy_threshold = 4000
        self.r_keyword.pause_threshold = 0.3
        self.r_keyword.non_speaking_duration = 0.1

        self.stop_listening_keyword = None

        self.run_listen = True
        self.keywords = [("cristal", 1), ("hey cristal", 1), ("ey cristal", 1), ("christal", 1) ]

        self.set_microphone()

    def set_microphone(self):
        #for device_index in sr.Microphone.list_working_microphones():
        #    self.mic = sr.Microphone(device_index=device_index)
        #    break
        #else:
        self.mic = sr.Microphone(chunk_size=2048)
        #    print("No working microphones found!")

    def callback(self, recognizer, audio):
        try:
            print("Estoy escuchando")
            speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=self.keywords, language="es")
            print(speech_as_text)
            self.recognize_main()
        except sr.UnknownValueError as e:
            print("Palabra no procesada: ", e)
        except Exception as e:
            print(e)
    
    def recognize_main(self):
        print("Recognizing Main...")
        audio_data = self.r_main.listen(self.mic)
        data = self.r_main.recognize_google(audio_data, language="es-ES")
        print(data)

    def stop(self):
        self.run_listen = False
        self.stop_listening_keyword(wait_for_stop=False)

    def run(self):
        with self.mic as source:
            self.r_keyword.adjust_for_ambient_noise(source)
            self.r_main.adjust_for_ambient_noise(source)
        print("Iniciando...")
        self.stop_listening_keyword = self.r_keyword.listen_in_background(self.mic, self.callback)
        while self.run_listen: 
            time.sleep(0.1) 