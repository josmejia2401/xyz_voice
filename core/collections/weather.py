import requests
from utils.settings import WEATHER_API
from core.skill import AssistantSkill


class WeatherSkills(AssistantSkill):
    
    @classmethod
    def tell_the_weather(cls, ext = None, template = None, values = None, history = []):
        try:
            if WEATHER_API['KEY']:
                city = cls._get_city()
                if city:
                    temperature, temperature_min, temperature_max = cls._get_weather_status_and_temperature(city)
                    if temperature and temperature_min and temperature_max:
                        r = template.format("La temperatura actual para bogotá es %0.1f centigrados, temperatura mínima de %0.1f centigrados y temperatura máxima de %0.1f centigrados" % (temperature, temperature_min, temperature_max))
                    else:
                        r = template.format("Lo siento, en este momento no hay datos del tiempo.")
                else:
                    r = template.format("Lo siento, en este momento no hay datos de tu localización.")
            else:
                r = template.format("Por favor define la llave de open weather map.")
            
            cls.response(r)
        except Exception as e:
            r = template.format("En este momento no pude obtener datos del tiempo.")
            cls.response(r)
    """
    {
        "coord":{
            "lon":-74.08,
            "lat":4.61
        },
        "weather":[
            {
                "id":803,
                "main":"Clouds",
                "description":"nubes rotas",
                "icon":"04d"
            }
        ],
        "base":"stations",
        "main":{
            "temp":18,
            "feels_like":12.72,
            "temp_min":18,
            "temp_max":18,
            "pressure":1029,
            "humidity":45
        },
        "visibility":10000,
        "wind":{
            "speed":6.2,
            "deg":130
        },
        "clouds":{
            "all":75
        },
        "dt":1601057296,
        "sys":{
            "type":1,
            "id":8582,
            "country":"CO",
            "sunrise":1601030689,
            "sunset":1601074246
        },
        "timezone":-18000,
        "id":3688689,
        "name":"Bogotá",
        "cod":200
        }
    """
    @classmethod
    def _get_weather_status_and_temperature(cls, city):
        url = WEATHER_API["URL"].format(city, WEATHER_API["UNITS"], WEATHER_API["LANG"], WEATHER_API['KEY'])
        r = requests.get(url=url)
        if r.status_code == 200:
            rx = r.json()
            if rx["main"]:
                return rx["main"]["temp"], rx["main"]["temp_min"], rx["main"]["temp_max"]
        return None, None, None

    @classmethod
    def _get_city(cls):
        city = "bogota"
        return city