from gtts import gTTS
from playsound import playsound

class Speak(object):

    def __init__(self):
        super().__init__()
        self.OUTPUT_VAL = 0
    
    def get_name_output(self) -> str:
        self.OUTPUT_VAL += 1
        return "output/audio/AUDIO_{}.mp3".format(self.OUTPUT_VAL)

    def run(self, audioString):
        print("speaking {}".format(audioString))
        self.tts = gTTS(text=audioString, lang='es-ES')
        name = self.get_name_output()
        self.tts.save(name)
        playsound(name)