import sys
import time
from datetime import datetime
from category.skill import AssistantSkill

class ActivationSkills(AssistantSkill):

    @classmethod
    def enable_assistant(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        Plays activation sound and creates the assistant response according to the day hour.
        """
        pass

    @classmethod
    def disable_assistant(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        - Clear console
        - Shutdown the assistant service
        """
        cls.response('adiós')

    @classmethod
    def assistant_greeting(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        Assistant greeting based on day hour.
        """
        now = datetime.now()
        day_time = int(now.strftime('%H'))

        if day_time < 12:
            cls.response('Buenos días mi señor')
        elif 12 <= day_time < 18:
            cls.response('Buenas tardes mi señor')
        else:
            cls.response('Buenas noches mi señor')
