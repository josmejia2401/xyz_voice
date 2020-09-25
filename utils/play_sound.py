import multiprocessing
from playsound import playsound

def playx(path_file):
    playsound(path_file, True)

class PlayAudio:
    p = None

    @staticmethod
    def play(path_file):
        PlayAudio.stop()
        PlayAudio.p = multiprocessing.Process(target=playx, args=(path_file,))
        PlayAudio.p.start()

    @staticmethod
    def stop():
        if PlayAudio.p:
            PlayAudio.p.terminate()


PlayAudio.play("somethingToSay.mp3")

"""import pyaudio
import wave
import time
from pydub import AudioSegment

class PlayAudio(object):

    def __init__(self):
        super().__init__()
        # instantiate PyAudio
        self.p = None
        self.stream = None
        self.wf = None

    # define callback
    def callback(self, in_data, frame_count, time_info, status):
        data = self.wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    def play(self, path_file):
        if not self.stream or self.stream.is_stopped():
            dest = path_file
            if "mp3" in path_file:
                sound = AudioSegment.from_mp3(path_file)
                dest = path_file.replace(".mp3", ".wav")
                sound.export(dest, format="wav")

            self.p = pyaudio.PyAudio()
            # you audio here
            self.wf = wave.open(dest, 'rb')
            # open stream using callback
            self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                            channels=self.wf.getnchannels(),
                            rate=self.wf.getframerate(),
                            output=True,
                            stream_callback=self.callback)
            # start the stream
            self.stream.start_stream()
            while self.stream.is_active():
                pass
    
    def stop(self):
        if self.stream and self.stream.is_active():
            self.stream.stop_stream()
            self.stream.close()
            self.wf.close()
            self.p.terminate()
#stream.is_stopped()
"""
#a = PlayAudio()
#a.play("demo.wav")