from core.collections.activation import ActivationSkills
from core.collections.general import UtilSkills
from core.collections.datetime import DatetimeSkills
from core.collections.internet import InternetSkills
from core.collections.redimer import ReminderSkills
from core.collections.internet import InternetSkills
from core.collections.math import MathSkills
from core.collections.weather import WeatherSkills
from utils.mapping import math_tags

CONTROL_SKILLS = [
    {
        "func": ActivationSkills.assistant_greeting,
        "pattern": [".*buenos dias.*", ".*buenas tardes.*", ".*buenas noches.*"],
        "templates": ["{}"],
        "tags": "iniciar,hola,buenas tardes,buenos dias,buenas noches",
        "description": "Comandos para activar el sistema"
    },

    {
        "func": ActivationSkills.disable_assistant,
        "pattern": [],
        "templates": ["{}"],
        "tags": "deshabilitar asistente,deshabilitar sistema,pausar asistente,pausar sistema,dejar de escuchar,dormir asistente",
        "description": "Poner el sistema en pausa"
    }
]

BASIC_SKILLS = [
    {
        "enable": True,
        "pattern": [".*que hora es.*", ".*que hora.*", ".*hora actual.*"],
        "templates": ["{}", "la hora actual es {}"],
        "func": DatetimeSkills.tell_the_time,
        "tags": "que hora es,que hora,hora es,hora actual",
        "description": "Dice la hora actual"
    },

    {
        "enable": True,
        "pattern": [".*fecha actual.*", ".*dia es hoy.*"],
        "templates": ["{}", "hoy es {}"],
        "func": DatetimeSkills.tell_the_date,
        "tags": "fecha actual,que dia es hoy,dia es hoy",
        "description": "Dice la fecha actual"
    },
    {
        "enable": True,
        "pattern": [".*detener ahora.*", ".*detener cancion.*", ".*detener audio.*", ".*detener sonido.*", ".*de tener ahora.*", ".*de tener cancion.*", ".*de tener audio.*", ".*de tener sonido.*", ".*parar ahora.*", ".*parar cancion.*", ".*parar audio.*", ".*parar sonido.*"],
        "templates": ["se detiene la reproduccion actual", "se detiene el sonido"],
        "func": UtilSkills.speech_interruption,
        "tags": "detener ahora,detener reproduccion,detener cancion,detener audio,detener asistente",
        "description": "detiene la reproducción actual"
    },
    {
        "enable": True,
        "pattern": [".*subir volumen.*", ".*incrementar volumen.*", ".*aumentar volumen.*"],
        "templates": ["He subido el volumen"],
        "func": UtilSkills.increase_master_volume,
        "tags": "subir volumen,incrementar volumen,subir volumen otra vez,subir volumen nuevamente,aumentar volumen",
        "description": "Sube el volumen"
    },

    {
        "enable": True,
        "pattern": [".*reducir volumen.*", ".*bajar volumen.*", ".*disminuir volumen.*"],
        "templates": ["He bajado el volumen"],
        "func": UtilSkills.reduce_master_volume,
        "tags": "bajar volumen,disminuir volumen,bajar volumen otra vez,bajar volumen nuevamente",
        "description": "Decrementa el volumen"
    },

    {
        "enable": True,
        "pattern": [".*silenciar volumen.*", ".*bajar todo el volumen.*", ".*silencinar el volumen.*", ".*bajar todo volumen.*"],
        "templates": ["He silenciado el volumen"],
        "func": UtilSkills.mute_master_volume,
        "tags": "silenciar volumen,bajar todo el volumen,silenciar el volumen",
        "description": "Silencia el volumen"
    },

    {
        "enable": True,
        "pattern": [".*volumen al maximo.*", ".*volumen total.*", ".*volumen al 100.*", ".*volumen maximo.*"],
        "templates": ["He puesto el volumen al maximo"],
        "func": UtilSkills.max_master_volume,
        "tags": "volumen al maximo,volumen total,volumen al 100,volumen al cien,maximo volumen,volumen maximo",
        "description": "maximo volumen"
    },

    {
        "enable": True,
        "pattern": [".*volumen actual.*", ".*volumen en este momento.*", ".*porcentaje de volumen.*", ".*porcentaje volumen.*"],
        "templates": ["He subido el volumen"],
        "func": UtilSkills.current_master_volume,
        "tags": "volumen actual,volumen en este momento,actual volumen,porcentaje volumen,porcentaje de volumen",
        "description": "Actual volumen"
    },

    {
        "enable": True,
        "pattern": [".*conexion a internet.*",".*internet actual.*",".*hay internet.*",".*conexion internet.*",".*revisar internet.*"],
        "templates": ["{}"],
        "func": InternetSkills.internet_availability,
        "tags": "conexion a internet,internet actual,hay internet,conexion internet,revisar internet",
        "description": "Revisar conexión a internet"
    },
    {
        "enable": True,
        "pattern": [".*crear recordatorio.*",".*recordatorio en.*",".*recordar esto.*",".*recordar lo siguiente.*"],
        "templates": ["He creado el recordatorio en {}"],
        "func": ReminderSkills.create_reminder,
        "tags": "crear recordatorio,recordatorio en,recordar esto,recordar lo siguiente",
        "description": "Recordatorio"
    },
    {
        "enable": True,
        "pattern": [".*crear alarma.*",".*alarma en.*",".*agregar alarma.*",".*establecer alarma.*"],
        "templates": ["He creado la alarma en {}"],
        "func": ReminderSkills.set_alarm,
        "tags": "crear alarma,alarma en,agregar alarma,establecer alarma",
        "description": "Alarma"
    },

    {
        "enable": True,
        "pattern": [".*deteneter alarma.*",".*apagar alarma.*",".*deten la alarma.*",".*detener todas las alarmas.*",".*apagar todas las alarmas.*",".*parar alarma.*"],
        "templates": ["He apagado las alarmas"],
        "func": ReminderSkills.stop_alarm,
        "tags": "deteneter alarma,apagar alarma,deten la alarma,detener todas las alarmas,apagar todas las alarmas,parar alarma,deten la alarma,parar todas las alarmas,de tener todas las alarmas,de tener alarmas",
        "description": "Detener Alarma"
    },

    {
        "enable": True,
        "pattern": [".*lista alarmas.*",".*listado de alarmas.*",".*listado de alarma.*",".*lista de alarmas.*",".*lista alarmas.*",".*lista alarma.*",".*cuales son las alarmas.*",".*alarmas actuales.*"],
        "templates": ["Alarma {}"],
        "func": ReminderSkills.list_from_alarms,
        "tags": "lista alarmas,listado de alarmas,listado de alarma,lista de alarmas,lista alarmas,lista alarma,cuales son las alarmas,alarmas actuales",
        "description": "Lista Alarma"
    },

    {
        "enable": True,
        "pattern": [""],
        "templates": ["Alarma {}"],
        "func": MathSkills.do_calculations,
        "tags": math_tags,
        "description": "Calculos"
    },

    {
        "enable": True,
        "pattern": [".*clima actual.*",".*datos del clima.*",".*informacion del clima.*",".*temperatura actual.*",".*temperatura de.*",".*estadisticas del clima.*"],
        "templates": ["{}"],
        "func": WeatherSkills.tell_the_weather,
        "tags": "clima actual,datos del clima,informacion del clima,temperatura actual,temperatura de,estadisticas del clima",
        "description": "Calculos"
    },
]

 
def get_skills():
    return BASIC_SKILLS + CONTROL_SKILLS