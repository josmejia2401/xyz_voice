import re
import time
import datetime
from spa2num.converter import to_number

from threading import Thread
from apscheduler.schedulers.background import BackgroundScheduler

from category.skill import AssistantSkill

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

    alarm_pending = []
    STOP = False
    
    @classmethod
    def stop_alarm(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        cls.STOP = True
        cls.response("Apagando todas las alarma. El proceso se hará en unos segundos.")

    @classmethod
    def list_from_alarms(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        for alarm in cls.alarm_pending:
            cls.response("Alarma en {} horas {} minutos".format(alarm[0], alarm[1]))
        else:
            cls.response("No hay alarmas disponibles")

    @classmethod
    def create_reminder(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        Creates a simple reminder for the given time interval (seconds or minutes or hours..)
        :param voice_transcript: string (e.g 'Make a reminder in 10 minutes')
        """
        voice_transcript = param1
        voice_transcript = cls._replace_words_with_numbers(voice_transcript)
        reminder_duration, scheduler_interval, variation = cls._get_reminder_duration_and_time_interval(voice_transcript)
        def reminder():
            cls.response("Hola, te recuerdo que el recordatorio {0} {1} ha pasado!".format(reminder_duration, variation))
            job.remove()
        try:
            if reminder_duration:
                scheduler = BackgroundScheduler()
                interval = {scheduler_interval: int(reminder_duration)}
                job = scheduler.add_job(reminder, 'interval', **interval)
                cls.response("He creado un recordatorio en {0} {1}".format(reminder_duration, variation))
                scheduler.start()
        except Exception as e:
            cls.response("No pude crear el recordatorio")

    @classmethod
    def set_alarm(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        # ------------------------------------------------
        # Current Limitations
        # ------------------------------------------------
        # - User can set alarm only for the same day
        # - Works only for specific format hh:mm
        # - Alarm sounds for 12 secs and stops, user can't stop interrupt it.
        #   -- Future improvement is to ring until user stop it.
        voice_transcript = param1
        cls.response("Estableciendo alarma... espera.")
        try:
            s = cls._replace_words_with_numbers(voice_transcript)
            timex = [int(s) for s in s.split(" ") if s.isdigit()]
            if timex and len(timex) > 1:
                alarm_hour = timex[0] #values_range=[0, 24]
                alarm_minutes = timex[1] #values_range=[0, 59])
                thread = Thread(target=cls._alarm_countdown, args=(alarm_hour, alarm_minutes))
                thread.start()
                #cls.response("Alarma establecida en {} horas {} minutos".format(alarm_hour, alarm_minutes))
            elif timex and len(timex) > 0:
                reminder_duration, scheduler_interval, variation = cls._get_reminder_duration_and_time_interval(s)
                if reminder_duration and scheduler_interval and variation:
                    alarm_hour = 0
                    alarm_minutes = 1
                    if "hours" in scheduler_interval:
                        alarm_hour = int(reminder_duration)
                    elif "minutes" in scheduler_interval:
                        alarm_minutes = int(reminder_duration)
                    thread = Thread(target=cls._alarm_countdown, args=(alarm_hour, alarm_minutes))
                    thread.start()
                    #cls.response("Alarma establecida en {} horas {} minutos".format(alarm_hour, alarm_minutes))
                else:
                    cls.response("No se pudo establecer la alarma a las " + " ".join(timex))
            else:
                cls.response("No se pudo establecer la alarma a las " + " ".join(timex))
        except Exception as e:
            print(e)
            cls.response("No se pudo establecer la alarma.")

    @classmethod
    def _alarm_countdown(cls, alarm_hour: int, alarm_minutes: int):
        cls.alarm_pending.append([alarm_hour, alarm_minutes])
        cls.STOP == False
        now = datetime.datetime.now()
        alarm_time = now + datetime.timedelta(hours=alarm_hour, minutes=alarm_minutes, seconds=0, days=0)
        strTime = alarm_time.strftime("%A %d de %B de %Y a las %H y %M")
        fechaText = "La alarma sonará el {}".format(strTime)
        cls.response(fechaText)
        while alarm_time > now:
            if cls.STOP == True:
                cls.alarm_pending.remove([alarm_hour, alarm_minutes])
                return
            now = datetime.datetime.now()
            time.sleep(1)
        cls.STOP = False
        cls.alarm_pending.remove([alarm_hour, alarm_minutes])
        cls.response("sonando alarma!!!")

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