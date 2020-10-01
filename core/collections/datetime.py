from datetime import datetime, date
from core.skill import AssistantSkill

hour_mapping = {
                '0': 'cero',
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
    def tell_the_time(cls, ext = None, template = None, values = None, history = []):
        try:
            now = datetime.now()
            hour, minute = now.hour, now.minute
            converted_time = cls._time_in_text(hour, minute)
            response = template.format(converted_time)
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response

        except Exception as e:
            print("ActivationSkills.assistant_greeting", e)
            response = template.format("No se pudo procesar el comando")
            history_elem = cls.new_history(ext ,response)
            history.append(history_elem)
            cls.response(response)
            return response

    @classmethod
    def tell_the_date(cls, ext = None, template = None, values = None, history = []):
        """
        Tells ths current date
        """
        currentDate = datetime.now()
        strTime = currentDate.strftime("%A %d de %B de %Y")
        return template.format(strTime)

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