#!/usr/bin/env python3
from engines.stt import STTEngine
from observerx.observerx import Observer
from category.analyzer import SkillAnalyzer
from category.registry import get_func_from_skills
"""
Espera unos segundos
Cristal listo!!! estoy escuhando.
"""
class Cristal(Observer):

    def __init__(self):
        super().__init__()
        self.skillAnalyzer = SkillAnalyzer()
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
        if subject._state < 11 and payload["success"] == True:
            skill = self.skillAnalyzer.extract(payload["transcription"])
            print("skill", skill)
            if skill:
                func = get_func_from_skills(skill)
                if func:
                    func()
                else:
                    pass
            else:
                pass

        self.run()

if __name__=='__main__':
    cristal = Cristal()
    cristal.run()






    