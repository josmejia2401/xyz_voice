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


class AlarmSkills(AssistantSkill):

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
            r = template.format("Se detienen todas las alarmas")
            cls.response(r)
        except Exception as e:
            r = template.format("No se pudo detener todas las alarmas")
            cls.response(r)

    @classmethod
    def list_all(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return
            if cls.alarm_pending:
                cls.response("Las alarmas son:")
                for alarm in cls.alarm_pending:
                    day_of_week = alarm["day_of_week"]
                    hour = alarm["hour"]
                    minute = alarm["minute"]
                    r = "semana: {} , hora: {} , minuto: {}".format(day_of_week, hour, minute)
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
            if cls.get_activation() == False:
                return
            #if isinstance(values, tuple):
            values_x = values[0]
            if isinstance(values_x, list):
                duration = values_x[0]
            else:
                duration = values_x

            duration = cls._replace_words_with_numbers(duration)

            if duration is not None:
                idx = get_id()
                scheduler_interval = 'minutes'
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls._alarm_minutes, 'interval', **interval, id=idx, args=[idx, duration])

                cls.alarm_pending.append({"id": idx, "job": job, "day_of_week": None, "hour": None, "minute": duration})

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
            if cls.get_activation() == False:
                return
            
            values_x = values[0]
            if isinstance(values_x, list):
                duration = values_x[0]
            else:
                duration = values_x

            duration = cls._replace_words_with_numbers(duration)
            
            if duration is not None:
                idx = get_id()
                scheduler_interval = 'hours'
                interval = {scheduler_interval: int(duration)}
                job = cls.scheduler.add_job(cls._alarm_hours, 'interval', **interval, id=idx, args=[idx, duration])

                cls.alarm_pending.append({"id": idx, "job": job, "day_of_week": None, "hour": duration, "minute": None})

                if not cls.scheduler.running:
                    cls.scheduler.start()

                r = template.format("He creado una alarma en {0} horas".format(duration))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear la alarma")
            cls.response(r)


    @classmethod
    def _alarm_range_am(cls, idx):
        cls.scheduler.remove_job(job_id=idx)
        for p in cls.alarm_pending:
            if p["id"] == idx:
                cls.alarm_pending.remove(p)
                break
        cls.response("SONANDO ALARMA")

    @classmethod
    def create_alarm_range_time_week_am(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return
            #hora, minuto, rango ini, rango fin
            values_x = values[0]
            if isinstance(values_x, list):
                duration_h = values_x[0]
                duration_m = values_x[1]
                range_week_start = values_x[2]
                range_week_end = values_x[3]
            else:
                duration_h = values_x
                duration_m = values[1]
                range_week_start = values[2]
                range_week_end = values[3]

            duration_h = cls._replace_words_with_numbers(duration_h)
            duration_m = cls._replace_words_with_numbers(duration_m)
            
            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in range_week_start:
                        range_week_start = time_interval['scheduler_interval']
                        break
            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in range_week_end:
                        range_week_end = time_interval['scheduler_interval']
                        break

            if duration_h is not None and duration_m is not None:
                idx = get_id()

                m2 = str(duration_h) + ":" + str(duration_m) + " AM"
                m2 = cls._time_conversion(m2)
                m2 = m2.split(":")
                duration_h = m2[0].strip()
                duration_m = m2[1].strip()
                day_of_week = range_week_start + "-" + range_week_end

                cron1 = CronTrigger(day_of_week=day_of_week, hour=duration_h, minute=duration_m, timezone='America/Bogota')
                trigger = OrTrigger([cron1])

                job = cls.scheduler.add_job(cls._alarm_range_am, trigger, id=idx, args=[idx])

                cls.alarm_pending.append({"id": idx, "job": job, "day_of_week": day_of_week, "hour": duration_h, "minute": duration_m})

                if not cls.scheduler.running:
                    cls.scheduler.start()
                r = template.format("He creado la alarma {0} {1} {2} am".format(day_of_week, duration_h, duration_m))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear la alarma")
            cls.response(r)

    
    @classmethod
    def create_alarm_range_week_time_am(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return
            #hora, minuto, rango ini, rango fin
            values_x = values[0]
            if isinstance(values_x, list):
                range_week_start = values_x[0]
                range_week_end = values_x[1]
                duration_h = values_x[2]
                duration_m = values_x[3]
            elif isinstance(values_x, tuple):
                range_week_start = values_x[0]
                range_week_end = values_x[1]
                duration_h = values_x[2]
                duration_m = values_x[3]
            else:
                range_week_start = values[0]
                range_week_end = values[1]
                duration_h = values[2]
                duration_m = values[3]

            duration_h = cls._replace_words_with_numbers(duration_h)
            duration_m = cls._replace_words_with_numbers(duration_m)
            
            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in range_week_start:
                        range_week_start = time_interval['scheduler_interval']
                        break
            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in range_week_end:
                        range_week_end = time_interval['scheduler_interval']
                        break

            if duration_h is not None and duration_m is not None:
                idx = get_id()

                m2 = str(duration_h) + ":" + str(duration_m) + " AM"
                m2 = cls._time_conversion(m2)
                m2 = m2.split(":")
                duration_h = m2[0].strip()
                duration_m = m2[1].strip()
                day_of_week = range_week_start + "-" + range_week_end

                cron1 = CronTrigger(day_of_week=day_of_week, hour=duration_h, minute=duration_m, timezone='America/Bogota')
                trigger = OrTrigger([cron1])

                job = cls.scheduler.add_job(cls._alarm_range_am, trigger, id=idx, args=[idx])

                cls.alarm_pending.append({"id": idx, "job": job, "day_of_week": day_of_week, "hour": duration_h, "minute": duration_m})

                if not cls.scheduler.running:
                    cls.scheduler.start()
                r = template.format("He creado la alarma {0} {1} {2} am".format(day_of_week, duration_h, duration_m))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear la alarma")
            cls.response(r)



    @classmethod
    def _alarm_range_pm(cls, idx):
        cls.scheduler.remove_job(job_id=idx)
        for p in cls.alarm_pending:
            if p["id"] == idx:
                cls.alarm_pending.remove(p)
                break
        cls.response("SONANDO ALARMA")

    @classmethod
    def create_alarm_range_time_week_pm(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return
            #hora, minuto, rango ini, rango fin
            values_x = values[0]
            if isinstance(values_x, list):
                duration_h = values_x[0]
                duration_m = values_x[1]
                range_week_start = values_x[2]
                range_week_end = values_x[3]
            elif isinstance(values_x, tuple):
                duration_h = values_x[0]
                duration_m = values_x[1]
                range_week_start = values_x[2]
                range_week_end = values_x[3]
            else:
                duration_h = values[0]
                duration_m = values[1]
                range_week_start = values[2]
                range_week_end = values[3]

            duration_h = cls._replace_words_with_numbers(duration_h)
            duration_m = cls._replace_words_with_numbers(duration_m)
            
            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in range_week_start:
                        range_week_start = time_interval['scheduler_interval']
                        break
            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in range_week_end:
                        range_week_end = time_interval['scheduler_interval']
                        break

            if duration_h is not None and duration_m is not None:
                idx = get_id()

                m2 = str(duration_h) + ":" + str(duration_m) + " PM"
                m2 = cls._time_conversion(m2)
                m2 = m2.split(":")
                duration_h = m2[0].strip()
                duration_m = m2[1].strip()
                day_of_week = range_week_start + "-" + range_week_end

                cron1 = CronTrigger(day_of_week=day_of_week, hour=duration_h, minute=duration_m, timezone='America/Bogota')
                trigger = OrTrigger([cron1])

                job = cls.scheduler.add_job(cls._alarm_range_pm, trigger, id=idx, args=[idx])

                cls.alarm_pending.append({"id": idx, "job": job, "day_of_week": day_of_week, "hour": duration_h, "minute": duration_m})

                if not cls.scheduler.running:
                    cls.scheduler.start()
                r = template.format("He creado la alarma {0} {1} {2} pm".format(day_of_week, duration_h, duration_m))
                cls.response(r)
        except Exception as e:
            print(e)
            r = template.format("No se pudo crear la alarma")
            cls.response(r)

    
    @classmethod
    def create_alarm_range_week_time_pm(cls, ext=None, template=None, values=None, history=[]):
        try:
            if cls.get_activation() == False:
                return
            #hora, minuto, rango ini, rango fin
            values_x = values[0]
            if isinstance(values_x, list):
                range_week_start = values_x[0]
                range_week_end = values_x[1]
                duration_h = values_x[2]
                duration_m = values_x[3]
            elif isinstance(values_x, tuple):
                range_week_start = values_x[0]
                range_week_end = values_x[1]
                duration_h = values_x[2]
                duration_m = values_x[3]
            else:
                range_week_start = values[0]
                range_week_end = values[1]
                duration_h = values[2]
                duration_m = values[3]

            duration_h = cls._replace_words_with_numbers(duration_h)
            duration_m = cls._replace_words_with_numbers(duration_m)
            
            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in range_week_start:
                        range_week_start = time_interval['scheduler_interval']
                        break
            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in range_week_end:
                        range_week_end = time_interval['scheduler_interval']
                        break

            if duration_h is not None and duration_m is not None:
                idx = get_id()

                m2 = str(duration_h) + ":" + str(duration_m) + " PM"
                m2 = cls._time_conversion(m2)
                m2 = m2.split(":")
                duration_h = m2[0].strip()
                duration_m = m2[1].strip()
                day_of_week = range_week_start + "-" + range_week_end

                cron1 = CronTrigger(day_of_week=day_of_week, hour=duration_h, minute=duration_m, timezone='America/Bogota')
                trigger = OrTrigger([cron1])

                job = cls.scheduler.add_job(cls._alarm_range_pm, trigger, id=idx, args=[idx])

                cls.alarm_pending.append({"id": idx, "job": job, "day_of_week": day_of_week, "hour": duration_h, "minute": duration_m})

                if not cls.scheduler.running:
                    cls.scheduler.start()
                r = template.format("He creado la alarma {0} {1} {2} pm".format(day_of_week, duration_h, duration_m))
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