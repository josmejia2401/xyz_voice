import threading
from eventsx.listen import Listen
from eventsx.speak import Speak
from observerx.observerx import Observer
from category.mex import MeCategory
from category.joke import JokeCategory
from category.alarm import AlarmCategory
from category.timex import TimeCategory

class Cristal(Observer):

    def __init__(self):
        super().__init__()
        self.listen = Listen()
        self.speak = Speak()
        self.HISTORY = []
        self.CURRENT_CONTEXT = None
        #category
        self.me_category = MeCategory()
        self.joke_category = JokeCategory()
        self.alarm_category = AlarmCategory()
        self.time_category = TimeCategory()
    
    def get_model_path(self) -> str:
        from pocketsphinx import get_model_path
        model_path = get_model_path()
        return model_path

    def run(self):
        try:
            self.listen.attach(self)
            self.listen.run()
        except KeyboardInterrupt as e:
            self.me_category.stop()
            self.joke_category.stop()
            self.alarm_category.stop()
            self.time_category.top()
        except Exception as e:
            self.me_category.stop()
            self.joke_category.stop()
            self.alarm_category.stop()
            self.time_category.top()

    def add_history(self, payload):
        self.HISTORY.append(payload)

    def speak_history(self, inputx, outputx):
        x = {
            "input" : inputx, 
            "output": outputx
        }
        print(x)
        self.speak.run(outputx)
        self.add_history(x)

    def process(self, payload):
        print(payload)
        if payload["success"] == True:
            x = ""
            if self.CURRENT_CONTEXT:
                x = self.CURRENT_CONTEXT.respond(payload)

            if x:
                self.speak_history(payload["transcription"], x)
                return

            x = self.me_category.respond(payload)
            if x:
                self.CURRENT_CONTEXT = self.me_category
                self.speak_history(payload["transcription"], x)
                return

            x = self.joke_category.respond(payload)
            if x:
                self.CURRENT_CONTEXT = self.joke_category
                self.speak_history(payload["transcription"], x)
                return

            x = self.alarm_category.respond(payload)
            if x:
                self.CURRENT_CONTEXT = self.alarm_category
                self.speak_history(payload["transcription"], x)
                return

            x = self.time_category.respond(payload)
            if x:
                self.CURRENT_CONTEXT = self.time_category
                self.speak_history(payload["transcription"], x)
                return
            
            self.speak_history(payload["transcription"], "evento no reconocido")
        else:
            self.speak.run(payload["error"])

    def update(self, subject, payload) -> None:
        if subject._state < 11:
            self.process(payload)

if __name__=='__main__':
    cristal = Cristal()
    cristal.run()