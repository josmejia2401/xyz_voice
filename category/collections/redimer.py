import re
import time
import datetime

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

    @classmethod
    def _get_reminder_duration_and_time_interval(cls, voice_transcript):
        """
        Extracts the duration and the time interval from the voice transcript.
        NOTE: If there are multiple time intervals, it will extract the first one.
        """
        for time_interval in time_intervals.values():
            for variation in time_interval['variations']:
                if variation in voice_transcript:
                    # Change '[0-9]'to '([0-9])' and now the skill is working
                    #reg_ex = re.search('([0-9])', voice_transcript)
                    #duration = reg_ex.group(1)
                    #print(x)
                    duration = re.findall('[0-9]+', voice_transcript)
                    return duration[0], time_interval['scheduler_interval'], variation

    @classmethod
    def create_reminder(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        Creates a simple reminder for the given time interval (seconds or minutes or hours..)
        :param voice_transcript: string (e.g 'Make a reminder in 10 minutes')
        """
        voice_transcript = param1
        reminder_duration, scheduler_interval, variation = cls._get_reminder_duration_and_time_interval(voice_transcript)
        def reminder():
            cls.response("Hola, te recuerdo que el recordatorio {0} {1} ha pasado!".format(reminder_duration, variation))
            job.remove()
        try:
            if reminder_duration:
                print("reminder_duration", reminder_duration)
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
            timex = [int(s) for s in str.split() if s.isdigit()]
            if timex and len(timex) > 1:
                alarm_hour = timex[0] #values_range=[0, 24]
                alarm_minutes = timex[1] #values_range=[0, 59])
                cls.alarm_pending.append([alarm_hour, alarm_minutes])
                thread = Thread(target=cls._alarm_countdown, args=(alarm_hour, alarm_minutes))
                thread.start()
            else:
                cls.response("No se pudo establecer la alarma a las " + " ".join(timex))
        except Exception as e:
            cls.response("No se pudo establecer la alarma.")

    @classmethod
    def _alarm_countdown(cls, alarm_hour, alarm_minutes):
        now = datetime.datetime.now()
        alarm_time = datetime.datetime.combine(now.date(), datetime.time(alarm_hour, alarm_minutes, 0))
        waiting_period = alarm_time - now
        if waiting_period < datetime.timedelta(0):
            # Choose 8PM today as the time the alarm fires.
            # This won't work well if it's after 8PM, though.
            cls.response('This time has past for today')
        else:
            cls.alarm_pending.remove([alarm_hour, alarm_minutes])
            # Successful setup message
            cls.response("alarma establecida a las {} y {}".format(alarm_hour, alarm_minutes))
            # Alarm countdown starts
            time.sleep((alarm_time - now).total_seconds())
            cls.response("Hora {0}".format(datetime.datetime.now().strftime('%H:%M')))
            cls.response("sonando alarma. levantante")
            