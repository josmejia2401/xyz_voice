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
               'scheduler_interval': 'mon'
               },
    'miercoles': {'variations': ['miercoles', 'miercole'],
                  'scheduler_interval': 'mon'
                  },
    'jueves': {'variations': ['jueves', 'jueve'],
               'scheduler_interval': 'mon'
               },
    'viernes': {'variations': ['viernes', 'vierne'],
                'scheduler_interval': 'mon'
                },
    'sabado': {'variations': ['sabado', 'sabados'],
               'scheduler_interval': 'mon'
               },
    'domingo': {'variations': ['domingo', 'domingos'],
                'scheduler_interval': 'mon'
                },
}

class ReminderSkills(AssistantSkill):
    scheduler = BackgroundScheduler()
    #sched = BlockingScheduler()
    alarm_pending = []


    @classmethod
    def stop_all_alarm(cls, ext=None, template=None, values=None, history = []):
        try:
            cls.scheduler.remove_all_jobs()
            cls.scheduler.shutdown()
            response = template.format("Se detienen todas las alarmas")
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response
        except Exception as e:
            response = template.format("No se pudo detener todas las alarmas")
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response

    @classmethod
    def list_from_alarms(cls, ext=None, template=None, values=None, history = []):
        try:
            if cls.alarm_pending:
                cls.response("Las alarmas son:")
                for alarm in cls.alarm_pending:
                    day_of_week = alarm["day_of_week"]
                    hout = alarm["hour"]
                    minute = alarm["minute"]
                    alarms = "{} {} {}".format(day_of_week, hout, minute)
                    cls.response(alarms)
                response = template.format("Se listaron todas las alarmas")
                history_elem = cls.new_history(ext ,response)
                history.append(history_elem)
                cls.response(response)
                return response
            else:
                response = template.format("No hay alarmas disponibles")
                history_elem = cls.new_history(ext ,response)
                history.append(history_elem)
                cls.response(response)
                return response
        except Exception as e:
            response = template.format("No se pudo listar las alarmas")
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response
        finally:


    @classmethod
    def create_reminder(cls, ext=None, template=None, values=None, history = []):
        voice_transcript = ext
        voice_transcript = cls._replace_words_with_numbers(voice_transcript)
        reminder_duration, scheduler_interval, variation = cls._get_reminder_duration_and_time_interval(voice_transcript)
        def reminder(idx):
            cls.scheduler.remove_job(job_id=idx)
            for p in cls.alarm_pending:
                if p["id"] == idx:
                    cls.alarm_pending.remove(p)
                    break
            cls.response("Hola, te recuerdo que el recordatorio {0} {1} ha pasado!".format(reminder_duration, variation))
        try:
            if reminder_duration:
                idx = "reminder_" + str(reminder_duration)
                interval = {scheduler_interval: int(reminder_duration)}
                job = cls.scheduler.add_job(reminder, 'interval', **interval, id=idx, args=[idx])
                cls.alarm_pending.append({"id": idx, "job": job})
                if not cls.scheduler.running:
                    cls.scheduler.start()
                response = template.format("He creado un recordatorio en {0} {1}".format(reminder_duration, variation))
                history_elem = cls.new_history(ext ,response)
                history.append(history_elem)
                cls.response(response)
                return response
        except Exception as e:
            print(e)
            response = template.format("No se pudo crear el recordatorio")
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response


    @classmethod
    def set_alarm_interval(cls, ext=None, template=None, values=None, history = []):
        def scheduled_task(idx):
            print("Sonando alarma...")
            #job.remove()
            for p in cls.alarm_pending:
                if p["id"] == idx:
                    cls.alarm_pending.remove(p)
                    break
            cls.scheduler.remove_job(job_id=idx)

        try:
            start_ = values[0]
            end_ = values[1]
            hour_ = values[2]
            minute_ = ""

            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in start_:
                        start_ = time_interval['scheduler_interval']
                        break

            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in end_:
                        end_ = time_interval['scheduler_interval']
                        break

            hour_ = cls._replace_words_with_numbers(hour_)
            if "y" in hour_:
                x = hour_.split("y")
                duration = re.findall('[0-9]+', x[0].strip())
                hour_ = str(duration)
                duration = re.findall('[0-9]+', x[1].strip())
                minute_ = str(duration)
            elif ":" in hour_:
                x = hour_.split(":")
                duration = re.findall('[0-9]+', x[0].strip())
                hour_ = str(duration)
                duration = re.findall('[0-9]+', x[1].strip())
                minute_ = str(duration)
            
            day_of_week = start_ + "-" + end_

            cron1 = CronTrigger(day_of_week=day_of_week, hour=hour_, minute=minute_, timezone='America/Bogota')
            trigger = OrTrigger([cron1])

            idx = "alarm_" + day_of_week + "_" + hour_ + "_" + minute_
            job = cls.scheduler.add_job(scheduled_task, trigger, id= idx, args=[idx])
            cls.alarm_pending.append({"id": idx, "job": job, "day_of_week" : day_of_week, "hour": hour_, "minute": minute_})
            if not cls.scheduler.running:
                cls.scheduler.start()
            
            response = template.format("He creado la alarma {0} {1} {2}".format(day_of_week, hour_, minute_))
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response
        except Exception as e:
            print(e)
            response = template.format("No se pudo crear la alarma")
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response


    @classmethod
    def set_alarm(cls, ext=None, template=None, values=None, history = []):
        def scheduled_task(idx):
            print("Sonando alarma...")
            for p in cls.alarm_pending:
                if p["id"] == idx:
                    cls.alarm_pending.remove(p)
                    break
            cls.scheduler.remove_job(job_id=idx)
        try:
            values = values[0]
            start_ = values[0]
            hour_ = values[1]
            minute_ = values[2]
            for time_interval in time_intervals.values():
                for variation in time_interval['variations']:
                    if variation in start_:
                        start_ = time_interval['scheduler_interval']
                        break
            hour_ = cls._replace_words_with_numbers(hour_)
            if "y" in hour_:
                x = hour_.split("y")
                duration = re.findall('[0-9]+', x[0].strip())
                hour_ = str(duration)
                duration = re.findall('[0-9]+', x[1].strip())
                minute_ = str(duration)
            elif ":" in hour_:
                x = hour_.split(":")
                duration = re.findall('[0-9]+', x[0].strip())
                hour_ = str(duration)
                duration = re.findall('[0-9]+', x[1].strip())
                minute_ = str(duration)
            day_of_week = start_
            cron1 = CronTrigger(day_of_week=day_of_week, hour=hour_, minute=minute_, timezone='America/Bogota')
            trigger = OrTrigger([cron1])
            idx = "alarm_" + day_of_week + "_" + hour_ + "_" + minute_
            job = cls.scheduler.add_job(scheduled_task, trigger, id= idx, args=[idx])
            cls.alarm_pending.append({"id": idx, "job": job})
            if not cls.scheduler.running:
                cls.scheduler.start()
            
            response = template.format("He creado la alarma {0} {1} {2}".format(day_of_week, hour_, minute_))
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response
        except Exception as e:
            print(e)
            response = template.format("No se pudo crear la alarma")
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response
        

    @classmethod
    def _replace_words_with_numbers(cls, transcript):
        transcript_with_numbers = ''
        for word in transcript.split():
            try:
                number = to_number(word)
                transcript_with_numbers += ' ' + str(number)
            except ValueError as e:
                # If word is not a number words it has 'ValueError'
                # In this case we add the word as it is
                transcript_with_numbers += ' ' + word
        return transcript_with_numbers

    @classmethod
    def _get_reminder_duration_and_time_interval(cls, voice_transcript):
        """
        Extracts the duration and the time interval from the voice transcript.
        NOTE: If there are multiple time intervals, it will extract the first one.
        """
        for time_interval in time_intervals.values():
            for variation in time_interval['variations']:
                if variation in voice_transcript:
                    duration = re.findall('[0-9]+', voice_transcript)
                    return duration[0], time_interval['scheduler_interval'], variation

        return None, None, None
