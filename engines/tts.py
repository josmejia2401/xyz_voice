#!/usr/bin/env python3
from gtts import gTTS
import time
import os
from subprocess import Popen, PIPE
import threading
from multiprocessing import Process

from pydub import AudioSegment
from pydub.playback import play

class P(Process):
    def __init__(self, filename):
        super(P, self).__init__()
        self.filename = filename

    def run(self):
        
        from playsound import playsound
        playsound( self.filename, block = True)

        p = Popen(args=['mpg321', '-q', self.filename], shell=False, stdout=PIPE, stderr=PIPE)
        while p.poll() != 0 or p.returncode != 0:
            if TTSEngine.stop_speaking == True:
                p.terminate()
                break
            time.sleep(0.5)

        
        music = AudioSegment.from_mp3(self.filename)
        play(music)
        

class MyClass(threading.Thread):
    def __init__(self, filename):
        threading.Thread.__init__(self)
        self.filename = filename

    def run(self):
        try:
            print(os.getpid())
            self.raise_exception()
            
            print(111111)
            from playsound import playsound
            playsound( self.filename, block = True)
            
        except Exception as e:
            print(e)
        
    def get_id(self):
        
        print(threading.current_thread().name)
        print(threading.get_ident())
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id

    def raise_exception(self): 
        import ctypes
        thread_id = self.get_id() 
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
            ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure') 

class TTSEngine(object):

    stop_speaking = False
    dir_path = os.path.dirname(os.path.realpath(__file__))
    
    @staticmethod
    def build_audio(message):
        if message:
            myobj = gTTS(text=message, lang="es", slow=False)
            filename = os.path.join(TTSEngine.dir_path, "speek.mp3")
            myobj.save(filename)
            return filename
        return None

    @staticmethod
    def play_audio(filename):
        p = Popen(args=['mpg321', '-q', filename], shell=False, stdout=PIPE, stderr=PIPE)
        #p = Popen(args=['mpg321', '-q', filename], stdout=PIPE)
        p.wait()
        while p.poll() != 0 or p.returncode != 0:
            if TTSEngine.stop_speaking == True:
                p.terminate()
                break
            time.sleep(0.5)
        TTSEngine.stop_speaking = False

    @staticmethod
    def play_text(message=None, asyncx = False):
        print(message)
        if message:
            if asyncx == False:
                f = TTSEngine.build_audio(message)
                TTSEngine.play_audio(f)
            else:
                f = TTSEngine.build_audio(message)
                myclass = MyClass(f)
                myclass.start()
                while myclass.is_alive():
                    if TTSEngine.stop_speaking == True:
                        break
                    time.sleep(0.5)
                TTSEngine.stop_speaking = False
