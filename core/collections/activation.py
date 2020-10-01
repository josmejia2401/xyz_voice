import sys
import time
from datetime import datetime
from core.skill import AssistantSkill

class ActivationSkills(AssistantSkill):

    @classmethod
    def enable_assistant(cls, ext = None, template = None, values = None, history = []):
        pass

    @classmethod
    def disable_assistant(cls, ext = None, template = None, values = None, history = []):
        pass

    @classmethod
    def assistant_greeting(cls, ext = None, template = None, values = None, history = []):
        try:
            response = ''
            now = datetime.now()
            day_time = int(now.strftime('%H'))
            if day_time < 12:
                response = template.format('Buenos días mi señor')
            elif 12 <= day_time < 18:
                response = template.format("Buenas tardes mi señor")
            else:
                response = template.format('Buenas noches mi señor')
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response
        except Exception as e:
            print("ActivationSkills.assistant_greeting", e)
            response = template.format("No se pudo procesar el comando")
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response
