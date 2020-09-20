import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
from playsound import playsound
from general import GeneralStatement, WikipediaStatement

class XYZRespond(object):

    def __init__(self):
        super().__init__()
        self.OUTPUT_VAL = 0
    
    def get_name_output(self) -> str:
        self.OUTPUT_VAL += 1
        return "AUDIO_{}.mp3".format(self.OUTPUT_VAL)
    def run(self, audioString):
        print(audioString)
        self.tts = gTTS(text=audioString, lang='es-ES')
        name = self.get_name_output()
        self.tts.save(name)
        playsound(name)

class XYZListen(object):

    def __init__(self):
        super().__init__()
        self.main_r = sr.Recognizer()
        self.main_r.energy_threshold = 4000
        self.main_r.pause_threshold = 0.5
        self.main_lang = "es-ES"

        self.keyword_r = sr.Recognizer()
        self.keyword_r.energy_threshold = 4000
        self.keyword_r.pause_threshold = 0.2
        self.keyword_r.non_speaking_duration = 0.2
        self.keyword_lang = "es"

        self.stop_listening_keyword = None

        self.run_listen = True
        self.keywords = [("cristal", 1), ("hey cristal", 1), ("ey cristal", 1), ("christal", 1) ]

        self.set_microphone()

        self.xyz_respond = XYZRespond()
        self.general_statement = GeneralStatement(self.xyz_respond, self)
        self.wikipedia_statement = WikipediaStatement(self.xyz_respond, self)

    def set_microphone(self):
        #for device_index in sr.Microphone.list_working_microphones():
        #    self.mic = sr.Microphone(device_index=device_index)
        #    break
        #else:
        self.mic = sr.Microphone(chunk_size=2048)
        #    print("No working microphones found!")

    def callback(self, recognizer, audio):
        try:
            print("Color azul")
            speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=self.keywords, language=self.keyword_lang)
            result = self.recognize_main()
            self.process_main(result)
        except sr.UnknownValueError as e:
            print("Color rojo ", e)
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        except Exception as e:
            print(e)
    
    def recognize_main(self) -> str:
        print("Color verde")
        audio_data = self.main_r.listen(self.mic)
        data = self.main_r.recognize_google(audio_data, language=self.main_lang)
        return data

    def process_main(self, data):
        print(data)
        if data:
            result = self.general_statement.respond(data.lower())
            if result == 0:
                result = self.wikipedia_statement.respond(data.lower())
            if result == 0:
                print("No procesado")
        else:
            print("comando no encontrado")
        

    def stop(self):
        self.run_listen = False
        self.stop_listening_keyword(wait_for_stop=False)
        print("Deteniendo...")
        time.sleep(10)

    def run(self):
        try:
            with self.mic as source:
                self.keyword_r.adjust_for_ambient_noise(source)
                self.main_r.adjust_for_ambient_noise(source)
            print("Iniciando...")
            self.stop_listening_keyword = self.keyword_r.listen_in_background(self.mic, self.callback)
            while self.run_listen: 
                time.sleep(0.1)
        except KeyboardInterrupt as e:
            self.stop()
        except Exception as e:
            print(e)