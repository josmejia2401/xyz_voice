#!/usr/bin/env python3
from engines.stt import STTEngine
from engines.tts import TTSEngine
from observerx.observerx import Observer
from core.kernel import Kernel
"""
Espera unos segundos
Cristal listo!!! estoy escuhando.

"""
class Cristal(Observer):

    def __init__(self):
        super().__init__()
        self.tTSEngine = TTSEngine()

    def loading(self):
        self.tTSEngine.play_text("Cargando sistema, por favor espera.", asyncx=True)
        self.sTTEngine = STTEngine()
        self.kernel = Kernel()
        self.sTTEngine.attach(self)
    
    def ready(self):
        self.tTSEngine.play_text("Estoy escuchando.", asyncx=True)

    def run(self):
        try:
            self.sTTEngine.run(already_activated=False)
        except KeyboardInterrupt as e:
            print(e)
            self.sTTEngine.stop()
        except Exception as e:
            print(e)
            self.sTTEngine.stop()

    def update(self, subject, payload) -> None:
        if subject._state < 11 and payload["success"] == True:
            print("transcription", payload["transcription"])
            self.kernel.respond(payload["transcription"])
        self.run()

if __name__=='__main__':
    cristal = Cristal()
    cristal.loading()
    cristal.ready()
    cristal.run()






    