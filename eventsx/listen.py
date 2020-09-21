import speech_recognition as sr
import time
import threading
from observerx.observerx import ConcreteSubject

class Listen(ConcreteSubject):

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
        self.keywords = [("cristal", 1), ("hey cristal", 1), ("ey cristal", 1), ("christal", 1)]
        self.set_microphone()

    def set_microphone(self):
        self.mic = sr.Microphone(chunk_size=1024)

    def mic_keyword(self):
        if not isinstance(self.keyword_r, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")
        if not isinstance(self.mic, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance") 
        self.stop_listening_keyword = self.keyword_r.listen_in_background(self.mic, self.callback_keyword)
        while self.run_listen:
            time.sleep(1)

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
        self.stop_listening_keyword(wait_for_stop=True)
        print("Deteniendo...")

    def add_processed_words(self, data):
        if data:
            self.some_business_logic(data)
    
    def run(self):
        try:
            print("Iniciando...")
            with self.mic as source:
                self.keyword_r.adjust_for_ambient_noise(source)
                self.main_r.adjust_for_ambient_noise(source)
            self.mic_keyword()
        except KeyboardInterrupt as e:
            self.stop()
        except Exception as e:
            print(e)
