import speech_recognition as sr
from threading import Thread,current_thread
import gi
from gi.repository import GObject as gobject

class MainThreadClass:
    def __init__(self, opts):
        self.recognizer = Recognizer()
        self.recognizer.connect('finished', self.recognizer_finished)
        self.recognizer.listen()

    def self.recognizer_finished:
        print current_thread()  // Child thread
        self.recognizer.pause()

class Recognizer(gobject.GObject):
    __gsignals__ = {
        'finished' : (gobject.SIGNAL_RUN_LAST, gobject.TYPE_NONE, (gobject.TYPE_STRING,))
    }
    def __init__(self):
        self.r = sr.Recognizer()
        self.m = sr.Microphone()
        with self.m as source: 
            self.r.adjust_for_ambient_noise(source)

    def callback(self, recognizer, audio):
        try:
            text = recognizer.recognize_sphinx(audio, "en-US", self.keywords, None)
            self.emit("finished", text)
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
            self.emit("finished", '')
        except sr.RequestError as e:
            print("Sphinx error; {0}".format(e))

    def listen(self):
        print current_thread()  // Main Thread
        self.stop_listening = self.r.listen_in_background(self.m, self.callback)

    def pause(self):
        print current_thread() // Child thread
        self.stop_listening()