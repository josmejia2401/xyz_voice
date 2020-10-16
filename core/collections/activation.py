#!/usr/bin/env python3
import sys
import time
from datetime import datetime
from core.skill import AssistantSkill

class ActivationSkills(AssistantSkill):

    @classmethod
    def enable_assistant(cls, ext = None, template = None, values = None, history = []):
        cls.set_activation(True)
        r = template.format("Se activa el asistente")
        cls.response(r)

    @classmethod
    def disable_assistant(cls, ext = None, template = None, values = None, history = []):
        cls.set_activation(False)
        r = template.format("Se desactiva el asistente")
        cls.response(r)

    @classmethod
    def assistant_greeting(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return

            r = ''
            now = datetime.now()
            day_time = int(now.strftime('%H'))
            if day_time < 12:
                r = template.format('Buenos días mi señor')
            elif 12 <= day_time < 18:
                r = template.format("Buenas tardes mi señor")
            else:
                r = template.format('Buenas noches mi señor')
            cls.response(r)
        except Exception as e:
            print("ActivationSkills.assistant_greeting", e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)
