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
    def tell_the_time(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        Tells ths current time
        """
        now = datetime.now()
        hour, minute = now.hour, now.minute
        converted_time = cls._time_in_text(hour, minute)
        horaText = 'Son las: {}'.format(converted_time)
        cls.response(horaText)

    @classmethod
    def tell_the_date(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        Tells ths current date
        """
        currentDate = datetime.now()
        strTime = currentDate.strftime("%A %d de %B de %Y")
        fechaText = "Hoy es {}".format(strTime)
        cls.response(fechaText)
        #print(cls.user_input())

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
        timex = "{} y {} minutos".format(cls._create_hour_period(hour), minute)
        return timex