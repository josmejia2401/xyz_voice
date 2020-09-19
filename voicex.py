
import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS
from playsound import playsound
from general import GeneralStatement
from process import XYZListen, XYZRespond

class XYZ(object):

    def __init__(self):
        super().__init__()
        self.xyz_respond = XYZRespond()
        self.xyz_listen = XYZListen()
        self.general_statement = GeneralStatement(self.xyz_respond, self.xyz_listen) 

    def respond(self, audioString):
        self.xyz_respond.run(audioString)

    def listen(self):
        return self.xyz_listen.run()

    def run(self):
        #time.sleep(2)
        self.respond("Hola, cómo estás?")
        while True:
            try:
                data = self.listen()
                data = self.general_statement.respond(data)
                #self.respond(data)
            except Exception as e:
                print(e)
                break

if __name__=='__main__':
    xyz = XYZ()
    xyz.run()