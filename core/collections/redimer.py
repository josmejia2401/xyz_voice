import re
import time
import datetime
from spa2num.converter import to_number

from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.combining import OrTrigger

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


class ReminderSkills(AssistantSkill):
    scheduler = BackgroundScheduler()
    alarm_pending = []

    @classmethod
    def stop_all_alarm(cls, ext=None, template=None, values=None, history=[]):
        if not cls.get_activation():
            return
        try:
            cls.scheduler.remove_all_jobs()
            cls.scheduler.shutdown()
            response = template.format("Se detienen todas las alarmas")
            cls.response(response)
        except Exception as e:
            response = template.format("No se pudo detener todas las alarmas")
            cls.response(response)

    @classmethod
    def list_from_alarms(cls, ext=None, template=None, values=None, history=[]):
        try:
            if not cls.get_activation():
                return
            if cls.alarm_pending:
                cls.response("Las alarmas son:")
                for alarm in cls.alarm_pending:
                    day_of_week = alarm["day_of_week"]
                    hout = alarm["hour"]
                    minute = alarm["minute"]
                    alarms = "{} {} {}".format(day_of_week, hout, minute)
                    cls.response(alarms)

                response = template.format("Se listaron todas las alarmas")
                cls.response(response)
            else:
                response = template.format("No hay alarmas disponibles")
                cls.response(response)
        except Exception as e:
            response = template.format("No se pudo listar las alarmas")
            cls.response(response)

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
            if not cls.get_activation():
                return

            values_x = values[0]
            action = values_x[0]
            duration = values_x[1]
            duration = cls._replace_words_with_numbers(duration)
            
            if duration:
                
                scheduler_interval = 'minutes'
                idx = "reminder_" + str(duration)
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls.reminder_minutes, 'interval', **interval, id=idx, args=[idx, action, duration])

                cls.alarm_pending.append({"id": idx, "job": job})
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
            if not cls.get_activation():
                return

            values_x = values[0]
            duration = values_x[0]
            action = values_x[1]
            duration = cls._replace_words_with_numbers(duration)
            
            if duration:
                
                scheduler_interval = 'minutes'
                idx = "reminder_" + str(duration)
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls.reminder_minutes, 'interval', **interval, id=idx, args=[idx, action, duration])

                cls.alarm_pending.append({"id": idx, "job": job})
                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {0} minutos".format(duration))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)


    @classmethod
    def reminder_hours(cls, idx, action , duration):
        cls.scheduler.remove_job(job_id=idx)
        for p in cls.alarm_pending:
            if p["id"] == idx:
                cls.alarm_pending.remove(p)
                break
        cls.response("RECORDATORIO: Te recuerdo {}".format(action))


    @classmethod
    def create_reminder_action_time_hours(cls, ext=None, template=None, values=None, history=[]):
        try:
            if not cls.get_activation():
                return

            values_x = values[0]
            action = values_x[0]
            duration = values_x[1]
            duration = cls._replace_words_with_numbers(duration)
            
            if duration:
                
                scheduler_interval = 'hours'
                idx = "reminder_" + str(duration)
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls.reminder_hours, 'interval', **interval, id=idx, args=[idx, action, duration])

                cls.alarm_pending.append({"id": idx, "job": job})
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
            if not cls.get_activation():
                return

            values_x = values[0]
            duration = values_x[0]
            action = values_x[1]
            duration = cls._replace_words_with_numbers(duration)
            
            if duration:
                
                scheduler_interval = 'hours'
                idx = "reminder_" + str(duration)
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls.reminder_hours, 'interval', **interval, id=idx, args=[idx, action, duration])

                cls.alarm_pending.append({"id": idx, "job": job})
                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {0} horas".format(duration))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)

    @classmethod
    def reminder_pm(cls, idx, action, out_time_h, out_time_m):
        cls.scheduler.remove_job(job_id=idx)
        for p in cls.alarm_pending:
            if p["id"] == idx:
                cls.alarm_pending.remove(p)
                break
        cls.response("RECORDATORIO: Te recuerdo {}".format(action))


    @classmethod
    def create_reminder_action_time_pm(cls, ext=None, template=None, values=None, history=[]):
        try:
            if not cls.get_activation():
                return

            values_x = values[0]
            action = values_x[0]
            duration = values_x[1]
            duration = cls._replace_words_with_numbers(duration)
            
            if duration:
                
                scheduler_interval = 'minutes'
                idx = "reminder_" + str(duration)
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls.reminder_minutes, 'interval', **interval, id=idx, args=[idx, action, duration])

                cls.alarm_pending.append({"id": idx, "job": job})
                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {0} minutos".format(duration))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear el recordatorio")
            cls.response(r)

    @classmethod
    def create_reminder_time_action_pm(cls, ext=None, template=None, values=None, history=[]):
        try:
            if not cls.get_activation():
                return

            values_x = values[0]
            duration_h = values_x[0]
            duration_m = values_x[1]
            action = values_x[2]

            duration_h = int(cls._replace_words_with_numbers(duration_h))
            duration_m = int(cls._replace_words_with_numbers(duration_m))
            
            if duration_h and duration_m:

                m2 = str(duration_h) + ":" + str(duration_m) + " PM"
                print("m2", m2)
                in_time = datetime.datetime.strptime(m2, "%I:%M %p")
                print("in_time", in_time)
                out_time_h = datetime.datetime.strftime(in_time, "%H")
                print("out_time_h", out_time_h)
                out_time_m = datetime.datetime.strftime(in_time, "%M")
                print("out_time_m", out_time_m)

                cron1 = CronTrigger(hour=out_time_h, minute=out_time_m, timezone='America/Bogota')
                trigger = OrTrigger([cron1])
                idx = "redimer_" + out_time_h + "_" + out_time_m

                job = cls.scheduler.add_job(cls.reminder_pm, trigger, id=idx, args=[idx, action, out_time_h, out_time_m])
                cls.alarm_pending.append({"id": idx, "job": job})

                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado un recordatorio en {0}:{} pm".format(duration_h, duration_m))
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