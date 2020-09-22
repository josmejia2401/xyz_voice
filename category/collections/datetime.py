from datetime import datetime, date
from category.skill import AssistantSkill

hour_mapping = {'0': 'doce',
                '1': 'uno',
                '2': 'dos',
                '3': 'tres',
                '4': 'cuatro',
                '5': 'cinco',
                '6': 'seis',
                '7': 'siete',
                '8': 'ocho',
                '9': 'nueve',
                '10': 'dies',
                '11': 'once',
                '12': 'doce',
                }


class DatetimeSkills(AssistantSkill):

    @classmethod
    def tell_the_time(cls, **kwargs):
        """
        Tells ths current time
        """
        now = datetime.now()
        hour, minute = now.hour, now.minute
        converted_time = cls._time_in_text(hour, minute)
        cls.response('Son las: {0}'.format(converted_time))

    @classmethod
    def tell_the_date(cls, **kwargs):
        """
        Tells ths current date
        """
        today = date.today()
        cls.response('Hoy es: {0}'.format(today))

    @classmethod
    def _get_12_hour_period(cls, hour):
        return 'pm' if 12 <= hour < 24 else 'am'

    @classmethod
    def _convert_12_hour_format(cls, hour):
        return hour - 12 if 12 < hour <= 24 else hour

    @classmethod
    def _create_hour_period(cls, hour):
        hour_12h_format = cls._convert_12_hour_format(hour)
        period = cls._get_12_hour_period(hour)
        return hour_mapping[str(hour_12h_format)] + ' ' + '(' + period + ')'

    @classmethod
    def _time_in_text(cls, hour, minute):
        if minute == 0:
            time = cls._create_hour_period(hour) + " en punto"
        elif minute == 15:
            time = cls._create_hour_period(hour) + " y cuarto"
        elif minute == 30:
            time = cls._create_hour_period(hour) + " y media"
        elif minute == 45:
            hour_12h_format = cls._convert_12_hour_format(hour + 1)
            period = cls._get_12_hour_period(hour)
            time = "un cuarto menos de las " + hour_mapping[str(hour_12h_format)] + ' ' + '(' + period + ')'
        elif 0 < minute < 30:
            time = str(minute) + " minutos más " + cls._create_hour_period(hour)
        else:
            hour_12h_format = cls._convert_12_hour_format(hour + 1)
            period = cls._get_12_hour_period(hour)
            time = str(60 - minute) + " minutos para " + hour_mapping[str(hour_12h_format)] + ' ' + '(' + period + ')'
        return time