import sys
import time
from datetime import datetime
from core.skill import AssistantSkill

class ActivationSkills(AssistantSkill):

    @classmethod
    def enable_assistant(cls, ext = None, template = None, values = None):
        """
        Plays activation sound and creates the assistant response according to the day hour.
        """
        pass

    @classmethod
    def disable_assistant(cls, ext = None, template = None, values = None):
        """
        - Clear console
        - Shutdown the assistant service
        """
        return template.format("adios")

    @classmethod
    def assistant_greeting(cls, ext = None, template = None, values = None):
        try:
            now = datetime.now()
            day_time = int(now.strftime('%H'))
            if day_time < 12:
                return template.format('Buenos días mi señor')
            elif 12 <= day_time < 18:
                return template.format("Buenas tardes mi señor")
            else:
                return template.format('Buenas noches mi señor')
        except Exception as e:
            print("assistant_greeting", e)
