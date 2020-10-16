#!/usr/bin/env python3
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

class ReminderSkills(AssistantSkill):

    scheduler = BackgroundScheduler()
    alarm_pending = []

    @classmethod
    def stop_all(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return
            cls.alarm_pending = []
            cls.scheduler.remove_all_jobs()
            cls.scheduler.shutdown()
            r = template.format("Se detienen todos los recordatorios")
            cls.response(r)
        except Exception as e:
            r = template.format("No se pudo detener todos los recordatorios")
            cls.response(r)

    @classmethod
    def list_all(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return
            if cls.alarm_pending:
                cls.response("Los recordatorios son:")
                for alarm in cls.alarm_pending:
                    action = alarm["action"]
                    r = "{}".format(action)
                    cls.response(r)
                r = template.format("Se listaron todos los recordatorios")
                cls.response(r)
            else:
                r = template.format("No hay recordatorios")
                cls.response(r)
        except Exception as e:
            r = template.format("No se pudo listar los recordatorios")
            cls.response(r)

    @classmethod
    def reminder_minutes(cls, idx, action , duration):
        cls.scheduler.remove_job(job_id=idx)
        for p in cls.alarm_pending:
            if p["id"] == idx:
                cls.alarm_pending.remove(p)
                break
        cls.response("RECORDATORIO: Te recuerdo {}".format(action))

    @classmethod
    def create_reminder_action_time_minutes(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return

            values_x = values[0]
            action = values_x[0]
            duration = values_x[1]
            duration = cls._replace_words_with_numbers(duration)
            
            if duration:
                idx = get_id()

                scheduler_interval = 'minutes'
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls.reminder_minutes, 'interval', **interval, id=idx, args=[idx, action, duration])

                cls.alarm_pending.append({"id": idx, "job": job, "action": action, "action": action})
                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {0} minutos".format(duration))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)

    @classmethod
    def create_reminder_time_action_minutes(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return

            values_x = values[0]
            duration = values_x[0]
            action = values_x[1]
            duration = cls._replace_words_with_numbers(duration)
            
            if duration:
                idx = get_id()

                scheduler_interval = 'minutes'
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls.reminder_minutes, 'interval', **interval, id=idx, args=[idx, action, duration])

                cls.alarm_pending.append({"id": idx, "job": job, "action": action})
                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {0} minutos".format(duration))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)


    @classmethod
    def _reminder_hours(cls, idx, action , duration):
        cls.scheduler.remove_job(job_id=idx)
        for p in cls.alarm_pending:
            if p["id"] == idx:
                cls.alarm_pending.remove(p)
                break
        cls.response("RECORDATORIO: Te recuerdo {}".format(action))


    @classmethod
    def create_reminder_action_time_hours(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return

            values_x = values[0]
            action = values_x[0]
            duration = values_x[1]
            duration = cls._replace_words_with_numbers(duration)
            
            if duration:
                idx = get_id()

                scheduler_interval = 'hours'
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls._reminder_hours, 'interval', **interval, id=idx, args=[idx, action, duration])

                cls.alarm_pending.append({"id": idx, "job": job, "action": action})
                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {0} horas".format(duration))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)

    @classmethod
    def create_reminder_time_action_hours(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return

            values_x = values[0]
            duration = values_x[0]
            action = values_x[1]
            duration = cls._replace_words_with_numbers(duration)
            
            if duration:
                idx = get_id()

                scheduler_interval = 'hours'
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls._reminder_hours, 'interval', **interval, id=idx, args=[idx, action, duration])

                cls.alarm_pending.append({"id": idx, "job": job, "action": action})
                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {0} horas".format(duration))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)

    @classmethod
    def _reminder_pm(cls, idx, action, m2_h, m2_m):
        cls.scheduler.remove_job(job_id=idx)
        for p in cls.alarm_pending:
            if p["id"] == idx:
                cls.alarm_pending.remove(p)
                break
        cls.response("RECORDATORIO: Te recuerdo {}".format(action))


    @classmethod
    def create_reminder_action_time_pm(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return

            values_x = values[0]
            action = values_x[0]
            duration_h = values_x[1]
            duration_m = values_x[2]

            duration_h = int(cls._replace_words_with_numbers(duration_h))
            duration_m = int(cls._replace_words_with_numbers(duration_m))
            
            if duration_h and duration_m:
                
                idx = get_id()

                m2 = str(duration_h) + ":" + str(duration_m) + " PM"
                m2 = cls._time_conversion(m2)
                m2 = m2.split(":")
                m2_h = m2[0].strip()
                m2_m = m2[1].strip()

                cron1 = CronTrigger(hour=m2_h, minute=m2_m, timezone='America/Bogota')
                trigger = OrTrigger([cron1])

                job = cls.scheduler.add_job(cls._reminder_pm, trigger, id=idx, args=[idx, action, m2_h, m2_m])
                cls.alarm_pending.append({"id": idx, "job": job, "action": action})

                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {0}:{} pm".format(duration_h, duration_m))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)

    @classmethod
    def create_reminder_time_action_pm(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return

            values_x = values[0]
            duration_h = values_x[0]
            duration_m = values_x[1]
            action = values_x[2]

            duration_h = int(cls._replace_words_with_numbers(duration_h))
            duration_m = int(cls._replace_words_with_numbers(duration_m))
            
            if duration_h and duration_m:
                idx = get_id()

                m2 = str(duration_h) + ":" + str(duration_m) + " PM"
                m2 = cls._time_conversion(m2)
                m2 = m2.split(":")
                m2_h = m2[0].strip()
                m2_m = m2[1].strip()
 
                cron1 = CronTrigger(hour=m2_h, minute=m2_m, timezone='America/Bogota')
                trigger = OrTrigger([cron1])

                job = cls.scheduler.add_job(cls._reminder_pm, trigger, id=idx, args=[idx, action, m2_h, m2_m])
                cls.alarm_pending.append({"id": idx, "job": job, "action": action})

                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {}:{} pm".format(duration_h, duration_m))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)


    @classmethod
    def reminder_am(cls, idx, action, m2_h, m2_m):
        cls.scheduler.remove_job(job_id=idx)
        for p in cls.alarm_pending:
            if p["id"] == idx:
                cls.alarm_pending.remove(p)
                break
        cls.response("RECORDATORIO: Te recuerdo {}".format(action))


    @classmethod
    def create_reminder_action_time_am(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return

            values_x = values[0]
            action = values_x[0]
            duration_h = values_x[1]
            duration_m = values_x[2]

            duration_h = int(cls._replace_words_with_numbers(duration_h))
            duration_m = int(cls._replace_words_with_numbers(duration_m))
            
            if duration_h and duration_m:

                m2 = str(duration_h) + ":" + str(duration_m) + " AM"
                m2 = cls._time_conversion(m2)
                m2 = m2.split(":")
                m2_h = m2[0].strip()
                m2_m = m2[1].strip()

                cron1 = CronTrigger(hour=m2_h, minute=m2_m, timezone='America/Bogota')
                trigger = OrTrigger([cron1])
                idx = "redimer_" + m2_h + "_" + m2_m

                job = cls.scheduler.add_job(cls.reminder_am, trigger, id=idx, args=[idx, action, m2_h, m2_m])
                cls.alarm_pending.append({"id": idx, "job": job, "action": action})

                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {}:{} am".format(duration_h, duration_m))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)

    @classmethod
    def create_reminder_time_action_am(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return

            values_x = values[0]
            duration_h = values_x[0]
            duration_m = values_x[1]
            action = values_x[2]

            duration_h = int(cls._replace_words_with_numbers(duration_h))
            duration_m = int(cls._replace_words_with_numbers(duration_m))
            
            if duration_h and duration_m:

                m2 = str(duration_h) + ":" + str(duration_m) + " AM"
                m2 = cls._time_conversion(m2)
                m2 = m2.split(":")
                m2_h = m2[0].strip()
                m2_m = m2[1].strip()

                cron1 = CronTrigger(hour=m2_h, minute=m2_m, timezone='America/Bogota')
                trigger = OrTrigger([cron1])
                idx = "redimer_" + m2_h + "_" + m2_m

                args = [idx, action, m2_h, m2_m]

                job = cls.scheduler.add_job(cls.reminder_am, trigger, id=idx, args=args)

                cls.alarm_pending.append({"id": idx, "job": job, "action": action})

                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {}:{} am".format(duration_h, duration_m))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)


    @classmethod
    def _replace_words_with_numbers(cls, transcript):
        transcript_with_numbers = ''
        for word in transcript.split():
            try:
                number = to_number(word)
                transcript_with_numbers += ' ' + str(number)
            except ValueError as e:
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