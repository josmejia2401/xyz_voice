from engines.tts import TTSEngine
from engines.stt import STTEngine

import locale
#locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
locale.setlocale(locale.LC_TIME, 'es_CO.utf8')

class AssistantSkill:
    """
    This class is the parent of all skill classes.
    """
    activation = True

    @classmethod
    def set_activation(cls, activation = True):
        AssistantSkill.activation = activation

    @classmethod
    def get_activation(cls):
        return AssistantSkill.activation

    @classmethod
    def set_stop_speaking(cls, stop_speaking = True):
        TTSEngine.stop_speaking = stop_speaking
        if stop_speaking == True:
            TTSEngine.stop_audio()
            TTSEngine.stop_song()

    @classmethod
    def get_stop_speaking(cls):
        return TTSEngine.stop_speaking


    @classmethod
    def response(cls, text):
        """
        The mode of the response depends on the output engine:
            - TTT Engine: The response is only in text
            - TTS Engine: The response is in voice and text
        """
        TTSEngine.play_text(text)

    @classmethod
    def play_sound(cls, filename, asyncx = False):
        """
        The mode of the response depends on the output engine:
            - TTT Engine: The response is only in text
            - TTS Engine: The response is in voice and text
        """
        TTSEngine.play_sound(filename, asyncx)

        

    @classmethod
    def user_input(cls):
        response = STTEngine._recognize_speech_from_mic(already_activated=True)
        return response

    @classmethod
    def new_history(cls, inputx, outputx):
        out = {
            "intput" : inputx,
            "output": outputx
        }
        return new_history
    @classmethod
    def extract_tags(cls, voice_transcript, tags):
        """
        This method identifies the tags from the user transcript for a specific skill.

        e.x
        Let's that the user says "hi jarvis!".
        The skill analyzer will match it with enable_assistant skill which has tags 'hi, hello ..'
        This method will identify the that the enabled word was the 'hi' not the hello.

        :param voice_transcript: string
        :param tags: string
        :return: set
        """

        try:
            transcript_words = voice_transcript.split()
            tags = tags.split(',')
            return set(transcript_words).intersection(tags)
        except Exception as e:
            return set()
