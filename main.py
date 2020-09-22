#!/usr/bin/env python3
from engines.stt import STTEngine
from observerx.observerx import Observer
"""
Espera unos segundos
Cristal listo!!! estoy escuhando.
"""
class Cristal(Observer):

    def __init__(self):
        super().__init__()
        self.sTTEngine = STTEngine()
        self.build()
    
    def build(self):
        self.sTTEngine.attach(self)

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
        if subject._state < 11:
            print("responder", payload)
            self.run()

if __name__=='__main__':
    cristal = Cristal()
    cristal.run()






    