import re
import time
import datetime
from spa2num.converter import to_number

from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler
#from apscheduler.schedulers.blocking import BlockingScheduler

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
}


class ReminderSkills(AssistantSkill):
    scheduler = BackgroundScheduler()
    #sched = BlockingScheduler()
    alarm_pending = []
    
    @classmethod
    def stop_alarm(cls, ext = None, template = None, values = None):
        #cls.scheduler.remove_all_jobs()
        return template.format("Apagando todas las alarma. El proceso se hará en unos segundos.")

    @classmethod
    def list_from_alarms(cls, ext = None, template = None, values = None):
        for alarm in cls.alarm_pending:
            return template.format("Alarma en {} horas {} minutos".format(alarm[0], alarm[1]))
        else:
            return template.format("No hay alarmas disponibles")

    @classmethod
    def create_reminder(cls, ext = None, template = None, values = None):
        """
        Creates a simple reminder for the given time interval (seconds or minutes or hours..)
        :param voice_transcript: string (e.g 'Make a reminder in 10 minutes')
        """
        voice_transcript = ext
        voice_transcript = cls._replace_words_with_numbers(voice_transcript)
        reminder_duration, scheduler_interval, variation = cls._get_reminder_duration_and_time_interval(voice_transcript)
        def reminder():
            return template.format("Hola, te recuerdo que el recordatorio {0} {1} ha pasado!".format(reminder_duration, variation))
            job.remove()
        try:
            if reminder_duration:
                
                interval = {scheduler_interval: int(reminder_duration)}
                job = cls.scheduler.add_job(reminder, 'interval', **interval)
                cls.scheduler.start()
                return template.format("He creado un recordatorio en {0} {1}".format(reminder_duration, variation))
        except Exception as e:
            return template.format("No pude crear el recordatorio")

    @classmethod
    def set_alarm(cls, ext = None, template = None, values = None):
        from apscheduler.triggers.cron import CronTrigger
        from apscheduler.triggers.combining import OrTrigger

        cron1 = CronTrigger(day_of_week='mon-fri', hour='8', minute='30,45', timezone='America/Chicago')
        cron2 = CronTrigger(day_of_week='mon-fri', hour='9-15', minute='*/15', timezone='America/Chicago')
        trigger = OrTrigger([cron1, cron2])
        cls.scheduler.add_job(scheduled_task, trigger)

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