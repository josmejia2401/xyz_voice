from category.collections.activation import ActivationSkills
from category.collections.general import UtilSkills
from category.collections.datetime import DatetimeSkills
from category.collections.internet import InternetSkills
from category.collections.redimer import ReminderSkills
from category.collections.internet import InternetSkills
from category.collections.math import MathSkills
from category.collections.weather import WeatherSkills

from utils.mapping import math_tags
# All available assistant skills
# Keys description:
#    - "enable": boolean (With True are the enabled skills)
#    - "func": The skill method in Skills
#    - "tags": The available triggering tags
#    - "description": skill description
CONTROL_SKILLS = [
    {
        "func": ActivationSkills.assistant_greeting,
        "tags": "iniciar,hola,buenas tardes,buenos dias,buenas noches",
        "description": "Comandos para activar el sistema"
    },

    {
        "func": ActivationSkills.disable_assistant,
        "tags": "deshabilitar asistente,deshabilitar sistema,pausar asistente,pausar sistema,dejar de escuchar,dormir asistente",
        "description": "Poner el sistema en pausa"
    }
]

BASIC_SKILLS = [
    {
        "enable": True,
        "func": DatetimeSkills.tell_the_time,
        "tags": "que hora es,que hora,hora es,hora actual",
        "description": "Dice la hora actual"
    },

    {
        "enable": True,
        "func": DatetimeSkills.tell_the_date,
        "tags": "fecha actual,que dia es hoy,dia es hoy",
        "description": "Dice la fecha actual"
    },
    {
        "enable": True,
        "func": UtilSkills.speech_interruption,
        "tags": "detener ahora,detener reproduccion,detener cancion,detener audio,detener asistente",
        "description": "detiene la reproducción actual"
    },
    {
        "enable": True,
        "func": UtilSkills.increase_master_volume,
        "tags": "subir volumen,incrementar volumen,subir volumen otra vez,subir volumen nuevamente",
        "description": "Sube el volumen"
    },

    {
        "enable": True,
        "func": UtilSkills.reduce_master_volume,
        "tags": "bajar volumen,disminuir volumen,bajar volumen otra vez,bajar volumen nuevamente",
        "description": "Decrementa el volumen"
    },

    {
        "enable": True,
        "func": UtilSkills.mute_master_volume,
        "tags": "silenciar volumen,bajar todo el volumen,silenciar el volumen",
        "description": "Silencia el volumen"
    },

    {
        "enable": True,
        "func": UtilSkills.max_master_volume,
        "tags": "volumen al maximo,volumen total,volumen al 100,volumen al cien,maximo volumen,volumen maximo",
        "description": "maximo volumen"
    },

    {
        "enable": True,
        "func": InternetSkills.internet_availability,
        "tags": "conexión a internet,internet actual,hay internet,conexión internet,revisar internet",
        "description": "Revisar conexión a internet"
    },
    {
        "enable": True,
        "func": ReminderSkills.create_reminder,
        "tags": "crear recordatorio,recordatorio en,recordar esto,recordar lo siguiente",
        "description": "Recordatorio"
    },
    {
        "enable": True,
        "func": ReminderSkills.set_alarm,
        "tags": "crear alarma,alarma en,agregar alarma,establecer alarma",
        "description": "Alarma"
    },
    {
        "enable": True,
        "func": MathSkills.do_calculations,
        "tags": math_tags,
        "description": "Calculos"
    },

    {
        "enable": True,
        "func": WeatherSkills.tell_the_weather,
        "tags": "clima actual,datos del clima,informacion del clima,temperatura actual,temperatura de,estadisticas del clima",
        "description": "Calculos"
    },


    
]


def get_func_from_skills(text):
    try:
        #text = " ".join(text)
        textx = " ".join(str(e).strip() for e in text)
        for skill in BASIC_SKILLS + CONTROL_SKILLS:
            new_skills = skill["tags"].split(",")
            for sk in new_skills:
                if sk.strip() in textx.strip():
                    func = skill["func"]
                    return func
    except Exception as e:
        print(e)
    return None
