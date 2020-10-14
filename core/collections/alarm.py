import re
import time
import datetime
from utils.text_number import to_number

from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import OrTrigger
import uuid
from core.skill import AssistantSkill

time_intervals = {
    'segundos': {'variations': ['segundos', 'segundo'],
                 'scheduler_interval': 'seconds'
                 },
    'minutos': {'variations': ['minutos', 'minuto'],
                'scheduler_interval': 'minutes'
                },
    'horas': {'variations': ['hora', 'horas'],
              'scheduler_interval': 'hours'
              },
    'mes': {'variations': ['mes', 'meses'],
            'scheduler_interval': 'months'
            },
    'año': {'variations': ['año', 'años'],
            'scheduler_interval': 'years'
            },
    'lunes': {'variations': ['lunes', 'lune'],
              'scheduler_interval': 'mon'
              },
    'martes': {'variations': ['martes', 'marte'],
               'scheduler_interval': 'tue'
               },
    'miercoles': {'variations': ['miercoles', 'miercole'],
                  'scheduler_interval': 'wed'
                  },
    'jueves': {'variations': ['jueves', 'jueve'],
               'scheduler_interval': 'thu'
               },
    'viernes': {'variations': ['viernes', 'vierne'],
                'scheduler_interval': 'fri'
                },
    'sabado': {'variations': ['sabado', 'sabados'],
               'scheduler_interval': 'sat'
               },
    'domingo': {'variations': ['domingo', 'domingos'],
                'scheduler_interval': 'sun'
                },
}

def get_id():
    uuid_x = str(uuid.uuid1())
    return uuid_x


class AlarmSkills(AssistantSkill):

    scheduler = BackgroundScheduler()
    alarm_pending = []

    @classmethod
    def stop_all(cls, ext=None, template=None, values=None, history=[]):
        try:
            if not cls.get_activation():
                return
            cls.alarm_pending = []
            cls.scheduler.remove_all_jobs()
            cls.scheduler.shutdown()
            r = template.format("Se detienen todas las alarmas")
            cls.response(r)
        except Exception as e:
            r = template.format("No se pudo detener todas las alarmas")
            cls.response(r)

    @classmethod
    def list_all(cls, ext=None, template=None, values=None, history=[]):
        try:
            if not cls.get_activation():
                return
            if cls.alarm_pending:
                cls.response("Las alarmas son:")
                for alarm in cls.alarm_pending:
                    action = alarm["action"]
                    r = "{}".format(action)
                    cls.response(r)
                r = template.format("Se listaron todas las alarmas")
                cls.response(r)
            else:
                r = template.format("No hay alarmas")
                cls.response(r)
        except Exception as e:
            r = template.format("No se pudo listar las alarmas")
            cls.response(r)

    @classmethod
    def _alarm_minutes(cls, idx, duration):
        cls.scheduler.remove_job(job_id=idx)
        for p in cls.alarm_pending:
            if p["id"] == idx:
                cls.alarm_pending.remove(p)
                break
        cls.response("SONANDO ALARMA")

    @classmethod
    def create_alarm_time_minutes(cls, ext=None, template=None, values=None, history=[]):
        try:
            if not cls.get_activation():
                return
            #if isinstance(values, tuple):
            values_x = values[0]
            if isinstance(values_x, list):
                duration = values_x[0]
            else:
                duration = values_x

            duration = cls._replace_words_with_numbers(duration)

            if duration:
                idx = get_id()
                scheduler_interval = 'minutes'
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls._alarm_minutes, 'interval', **interval, id=idx, args=[idx, duration])

                cls.alarm_pending.append({"id": idx, "job": job, "action": None, "duration" : duration})
                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado una alarma en {0} minutos".format(duration))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear la alarma")
            cls.response(r)

    @classmethod
    def _alarm_hours(cls, idx, duration):
        cls.scheduler.remove_job(job_id=idx)
        for p in cls.alarm_pending:
            if p["id"] == idx:
                cls.alarm_pending.remove(p)
                break
        cls.response("SONANDO ALARMA")


    @classmethod
    def create_alarm_time_hours(cls, ext=None, template=None, values=None, history=[]):
        try:
            if not cls.get_activation():
                return
            
            values_x = values[0]
            if isinstance(values_x, list):
                duration = values_x[0]
            else:
                duration = values_x

            duration = cls._replace_words_with_numbers(duration)
            
            if duration:
                idx = get_id()
                scheduler_interval = 'hours'
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls._alarm_hours, 'interval', **interval, id=idx, args=[idx, duration])

                cls.alarm_pending.append({"id": idx, "job": job, "action": None, "duration": duration})
                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado una alarma en {0} horas".format(duration))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear la alarma")
            cls.response(r)

    @classmethod
    def _replace_words_with_numbers(cls, transcript):
        transcript_with_numbers = ''
        for word in transcript.split():
            try:
                number = to_number(word)
                print(number)
                transcript_with_numbers += ' ' + str(number)
            except ValueError as e:
                print(e)
                transcript_with_numbers += ' ' + word
        return transcript_with_numbers
    
    @classmethod
    def _time_conversion(cls, s):
        if "PM" in s:
            s=s.replace("PM"," ")
            t= s.split(":")
            if t[0] != '12':
                t[0]=str(int(t[0])+12)
                s= (":").join(t)
            return s
        else:
            s = s.replace("AM"," ")
            t= s.split(":")
            if t[0] == '12':
                t[0]='00'
                s= (":").join(t)
            return s