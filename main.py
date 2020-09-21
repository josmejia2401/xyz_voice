import threading
from eventsx.listen import Listen
from eventsx.speak import Speak
from observerx.observerx import Observer
from category.mex import MeCategory
from category.joke import JokeCategory

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
    
    def get_model_path(self) -> str:
        from pocketsphinx import get_model_path
        model_path = get_model_path()
        return model_path

    def run(self):
        self.listen.attach(self)
        self.listen.run()

    def add_history(self, payload):
        self.HISTORY.append(payload)

    def speak_history(self, inputx, outputx):
        x = {
            "input" : inputx, 
            "output": outputx
        }
        self.speak.run(outputx)
        self.add_history(x)

    def process(self, payload):
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
        else:
            self.speak.run(payload["error"])

    def update(self, subject, payload) -> None:
        if subject._state < 11:
            self.process(payload)

if __name__=='__main__':
    cristal = Cristal()
    cristal.run()