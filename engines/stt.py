import speech_recognition as sr
from observerx.observerx import ConcreteSubject
import time
import threading

class STTEngine(ConcreteSubject):
    """
    Speech To Text Engine (STT)

    Google API Speech recognition settings
    SpeechRecognition API : https://pypi.org/project/SpeechRecognition/2.1.3
    """

    recognizer = sr.Recognizer()
    microphone = sr.Microphone(sample_rate=44100)
    # energía de audio mínima a considerar para la grabación
    recognizer.energy_threshold = 3000
    # segundos de audio sin hablar antes de que una frase se considere completa
    recognizer.pause_threshold = 0.8
    recognizer.dynamic_energy_threshold = True
    # segundos mínimos de audio hablado antes de que consideremos el audio hablado como una frase; los valores por debajo de esto se ignoran (para filtrar clics y estallidos)
    #self.recognizer.phrase_threshold = 0.3
    # segundos de audio que no habla para mantenerse en ambos lados de la grabación
    #self.recognizer.non_speaking_duration = 0.2

    main_lang = "es-ES"
    keyword_lang = "es"
    keywords = [("cristal", 1), ("hey cristal", 1), ("ey cristal", 1), ("christal", 1)]

    def __init__(self):
        super().__init__() 
        
    def run(self, already_activated=False):
        if not isinstance(self.recognizer, sr.Recognizer):
            raise TypeError("`recognizer` must be `Recognizer` instance")
        if not isinstance(self.microphone, sr.Microphone):
            raise TypeError("`microphone` must be `Microphone` instance")
        self.recognize_input(already_activated)
        
    def stop(self):
        print("Deteniendo...")

    def recognize_input(self, already_activated=False):
        response = STTEngine._recognize_speech_from_mic(already_activated)
        self.stop()
        self.some_business_logic(response)

    @classmethod
    def _recognize_speech_from_mic(cls, already_activated=False):
        print("escuchando")
        response = { "success": True, "error": None, "transcription": None }
        with cls.microphone as source:
            cls.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = cls.recognizer.listen(source)
        try:
            with open("microphone-results.wav", "wb") as f:
                f.write(audio.get_wav_data())

            #speech_as_text = recognizer.recognize_sphinx(audio, keyword_entries=self.keywords, language=self.keyword_lang)
            response["transcription"] = cls.recognizer.recognize_google(audio, language=cls.main_lang).lower()
            if already_activated == False and cls._activation_name_exist(response):
                response = cls._remove_activation_word(response)
            elif already_activated == True:
                pass
            else:
                response["success"] = False
        except sr.UnknownValueError:
            response["success"] = False
            response["transcription"] = "Función no conocida"
        except sr.RequestError:
            response["success"] = False
            response["transcription"] = "API no disponible en este momento."
        return response

    #@staticmethod
    @classmethod
    def _activation_name_exist(cls, transcript):
        if transcript["transcription"]:
            transcript_words = transcript["transcription"].split()
            names = []
            for name in cls.keywords:
                names.append(name[0])
            return bool(set(transcript_words).intersection(names))
        else:
            return False

    #@staticmethod
    @classmethod
    def _remove_activation_word(cls, transcript):
        for name in cls.keywords:
            count = transcript["transcription"].count(name[0])
            transcript["transcription"] = transcript["transcription"].replace(name[0], "", count)
        transcript["transcription"] = transcript["transcription"].strip()
        return transcript
