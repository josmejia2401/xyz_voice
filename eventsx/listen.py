#!/usr/bin/env python3
import speech_recognition as sr
import time
import threading
from observerx.observerx import ConcreteSubject

class Listen(ConcreteSubject):

    def __init__(self):
        super().__init__()
        self.main_r = sr.Recognizer()
        # energía de audio mínima a considerar para la grabación
        # para ubuntu
        # self.main_r.energy_threshold = 4500
        # para mac
        self.main_r.energy_threshold = 3000
        # segundos de audio sin hablar antes de que una frase se considere completa
        self.main_r.pause_threshold = 0.4
        self.main_r.dynamic_energy_threshold = False
         # segundos mínimos de audio hablado antes de que consideremos el audio hablado como una frase; los valores por debajo de esto se ignoran (para filtrar clics y estallidos)
        self.main_r.phrase_threshold = 0.2
        # segundos de audio que no habla para mantenerse en ambos lados de la grabación
        self.main_r.non_speaking_duration = 0.2
        self.main_lang = "es-ES"

        self.keyword_lang = "es"
        self.stop_listening_keyword = None
        self.run_listen = True
        self.keywords = [("cristal", 1), ("hey cristal", 1), ("ey cristal", 1), ("christal", 1)]
        self.set_microphone()

    def set_microphone(self):
        self.mic = sr.Microphone(chunk_size=1024)

    def mic_keyword(self):
        if not isinstance(self.main_r, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")
        if not isinstance(self.mic, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance") 
        self.stop_listening_keyword = self.main_r.listen_in_background(self.mic, self.callback_keyword)
        while self.run_listen:
            time.sleep(1)
        print("mic_keyword exiting")

    def callback_keyword(self, recognizer, audio):
        try:
            print("azul")
            speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=self.keywords, language=self.keyword_lang)
            response = self.recognize_main()
            self.add_processed_words(response)
        except sr.UnknownValueError as e:
            print("rojo ", e)
        except sr.RequestError as e:
            print("rojo; {0}".format(e))
        except Exception as e:
            print("rojo", e)
    
    def recognize_main(self) -> str:
        print("verde")
        audio = self.main_r.listen(self.mic)
        response = {
            "success": True,
            "error": None,
            "transcription": None
        }
        try:
            response["transcription"] = self.main_r.recognize_google(audio, language=self.main_lang)
        except sr.RequestError:
            response["success"] = False
            response["error"] = "API no disponible"
        except sr.UnknownValueError:
            response["success"] = False
            response["error"] = "función o evento no reconocido"
        return response

    def mic_main(self):
        if not isinstance(self.main_r, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")
        if not isinstance(self.mic, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")
        return self.recognize_main()

    def stop(self):
        self.run_listen = False
        self.stop_listening_keyword(wait_for_stop=False)
        print("Deteniendo...")

    def add_processed_words(self, data):
        if data:
            self.some_business_logic(data)
    
    def run(self):
        try:
            print("Iniciando...")
            with self.mic as source:
                #The ``duration`` parameter is the maximum number of seconds that it will dynamically adjust the threshold for before returning. This value should be at least 0.5 in order to get a representative sample of the ambient noise.
                self.main_r.adjust_for_ambient_noise(source, duration=0.4)
            self.mic_keyword()
        except KeyboardInterrupt as e:
            self.stop()
        except Exception as e:
            print(e)
