import threading
from eventsx.listen import Listen
from observerx.observerx import Observer

class Cristal(Observer):

    def __init__(self):
        super().__init__()
        self.listen = Listen()
    
    def get_model_path(self) -> str:
        from pocketsphinx import get_model_path
        model_path = get_model_path()
        return model_path

    def run(self):
        self.listen.attach(self)
        self.listen.run()

    def update(self, subject, payload) -> None:
        if subject._state < 11:
            print("Procesando palabra:::: " , payload)

if __name__=='__main__':
    cristal = Cristal()
    cristal.run()