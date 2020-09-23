
import threading
import queue
from gtts import gTTS
from playsound import playsound
import time


class TTSEngine(object):

    def __init__(self):
        super().__init__()
        self.message_queue = queue.Queue(maxsize=9)
        self.stop_speaking = False
        self.playing = False

    @classmethod
    def play_text(cls, message):
        if message:
            myobj = gTTS(text=message, lang="es", slow=False)
            myobj.save("somethingToSay.mp3")
            playsound('somethingToSay.mp3')

    def assistant_response(self, message):
        """
        Assistant response in voice.
        :param message: string
        """
        self._insert_into_message_queue(message)
        try:
            speech_tread = threading.Thread(target=self._speech_and_console)
            speech_tread.start()
        except RuntimeError as e:
            print('Error in assistant response thread with message {0}'.format(e))

    def _insert_into_message_queue(self, message):
        try:
            self.message_queue.put(message)
        except Exception as e:
            print("Unable to insert message to queue with error message: {0}".format(e))

    def _speech_and_console(self):
        """
        Speech method translate text batches to speech and print them in the console.
        :param text: string (e.g 'tell me about google')
        """
        try:
            while not self.message_queue.empty():
                if self.stop_speaking:
                    self.stop_speaking = False
                    break
                if self.playing == False:
                    self.playing = True
                    cumulative_batch = ''
                    message = self.message_queue.get()
                    TTSEngine.play_text(message)
                    break
                else:
                    time.sleep(0.5)
        except Exception as e:
            print("Speech and console error message: {0}".format(e))
        finally:
            self.playing = False