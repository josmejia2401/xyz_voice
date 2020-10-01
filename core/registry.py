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
        "description": "Comandos para activar el sistema",
        "context": "",
        "next": []
    },

    {
        "func": ActivationSkills.disable_assistant,
        "pattern": [".*deshabilitar asistente.*", ".*deshabilitar sistema.*", ".*pausar asistente.*", ".*pausar sistema.*", ".*dejar de escuchar.*", ".*dormir asistente.*"],
        "templates": ["{}"],
        "tags": "deshabilitar asistente,deshabilitar sistema,pausar asistente,pausar sistema,dejar de escuchar,dormir asistente",
        "description": "Poner el sistema en pausa",
        "context": "",
        "next": []
    }
]

BASIC_SKILLS = [
    {
        "enable": True,
        "pattern": [".*que hora es.*", ".*que hora.*", ".*hora actual.*"],
        "templates": ["{}", "la hora actual es {}"],
        "func": DatetimeSkills.tell_the_time,
        "tags": "que hora es,que hora,hora es,hora actual",
        "description": "Dice la hora actual",
        "context": "",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*fecha actual.*", ".*dia es hoy.*"],
        "templates": ["{}", "hoy es {}"],
        "func": DatetimeSkills.tell_the_date,
        "tags": "fecha actual,que dia es hoy,dia es hoy",
        "description": "Dice la fecha actual",
        "context": "",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*detener ahora.*", ".*detener cancion.*", ".*detener audio.*", ".*detener sonido.*", ".*de tener ahora.*", ".*de tener cancion.*", ".*de tener audio.*", ".*de tener sonido.*", ".*parar ahora.*", ".*parar cancion.*", ".*parar audio.*", ".*parar sonido.*"],
        "templates": ["se detiene la reproduccion actual", "se detiene el sonido"],
        "func": UtilSkills.speech_interruption,
        "tags": "detener ahora,detener reproduccion,detener cancion,detener audio,detener asistente",
        "description": "detiene la reproducción actual",
        "context": "",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*subir volumen.*", ".*incrementar volumen.*", ".*aumentar volumen.*", ".*subir volumen otra vez.*", ".*elevar volumen.*"],
        "templates": ["{}"],
        "func": UtilSkills.increase_master_volume,
        "tags": "subir volumen,incrementar volumen,subir volumen otra vez,subir volumen nuevamente,aumentar volumen",
        "description": "Sube el volumen",
        "context": "",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*reducir volumen.*", ".*bajar volumen.*", ".*disminuir volumen.*"],
        "templates": ["{}"],
        "func": UtilSkills.reduce_master_volume,
        "tags": "bajar volumen,disminuir volumen,bajar volumen otra vez,bajar volumen nuevamente",
        "description": "Decrementa el volumen",
        "context": "",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*silenciar volumen.*", ".*bajar todo el volumen.*", ".*silencinar el volumen.*", ".*bajar todo volumen.*"],
        "templates": ["{}"],
        "func": UtilSkills.mute_master_volume,
        "tags": "silenciar volumen,bajar todo el volumen,silenciar el volumen",
        "description": "Silencia el volumen",
        "context": "",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*volumen al maximo.*", ".*volumen total.*", ".*volumen al 100.*", ".*volumen maximo.*"],
        "templates": ["{}"],
        "func": UtilSkills.max_master_volume,
        "tags": "volumen al maximo,volumen total,volumen al 100,volumen al cien,maximo volumen,volumen maximo",
        "description": "maximo volumen",
        "context": "",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*volumen actual.*", ".*volumen en este momento.*", ".*porcentaje de volumen.*", ".*porcentaje volumen.*"],
        "templates": ["{}"],
        "func": UtilSkills.current_master_volume,
        "tags": "volumen actual,volumen en este momento,actual volumen,porcentaje volumen,porcentaje de volumen",
        "description": "Actual volumen",
        "context": "",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*conexion a internet.*", ".*internet actual.*", ".*hay internet.*", ".*conexion internet.*", ".*revisar internet.*"],
        "templates": ["{}"],
        "func": InternetSkills.internet_availability,
        "tags": "conexion a internet,internet actual,hay internet,conexion internet,revisar internet",
        "description": "Revisar conexión a internet",
        "context": "",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*crear recordatorio.*", ".*recordatorio en.*", ".*recordar esto.*", ".*recordar lo siguiente.*"],
        "templates": ["{}"],
        "func": ReminderSkills.create_reminder,
        "tags": "crear recordatorio,recordatorio en,recordar esto,recordar lo siguiente",
        "description": "Recordatorio",
        "context": "",
        "next": []
    },

    {
        "enable": True,
        "pattern": [
            ".*crear alarma de (.*) a (.*) a las (.*)", ".*alarma de (.*) a (.*) a las (.*)", ".*agregar alarma de (.*) a (.*) a las (.*)", ".*establecer alarma de (.*) a (.*) a las (.*)",
            ".*crear alarma (.*) a (.*) a las (.*)", ".*alarma (.*) a (.*) a las (.*)", ".*agregar alarma (.*) a (.*) a las (.*)", ".*establecer alarma (.*) a (.*) a las (.*)"
        ],
        "templates": ["He creado la alarma en {}"],
        "func": ReminderSkills.set_alarm_interval,
        "tags": "crear alarma,alarma en,agregar alarma,establecer alarma",
        "description": "Alarma",
        "context": "",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*crear alarma el (.*) a las (\d*):(\d*).*", ".*alarma el (*) a las (\d*):(\d*).*", ".*agregar alarma el(d*) a las (\d*):(\d*).*", ".*establecer alarma el(.*) a las (\d*):(\d*).*"],
        "templates": ["He creado la alarma en {}"],
        "func": ReminderSkills.set_alarm,
        "tags": "crear alarma,alarma en,agregar alarma,establecer alarma",
        "description": "Alarma",
        "context": "",
        "next": []
    },


    {
        "enable": True,
        "pattern": [".*deteneter alarma.*", ".*apagar alarma.*", ".*deten la alarma.*", ".*detener todas las alarmas.*", ".*apagar todas las alarmas.*", ".*parar alarma.*"],
        "templates": ["He apagado las alarmas"],
        "func": ReminderSkills.stop_all_alarm,
        "tags": "deteneter alarma,apagar alarma,deten la alarma,detener todas las alarmas,apagar todas las alarmas,parar alarma,deten la alarma,parar todas las alarmas,de tener todas las alarmas,de tener alarmas",
        "description": "Detener Alarma",
        "context": "",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*lista alarmas.*", ".*listado de alarmas.*", ".*listado de alarma.*", ".*lista de alarmas.*", ".*lista alarmas.*", ".*lista alarma.*", ".*cuales son las alarmas.*", ".*alarmas actuales.*"],
        "templates": ["{}"],
        "func": ReminderSkills.list_from_alarms,
        "tags": "lista alarmas,listado de alarmas,listado de alarma,lista de alarmas,lista alarmas,lista alarma,cuales son las alarmas,alarmas actuales",
        "description": "Lista Alarma",
        "context": "",
        "next": []
    },


    {
        "enable": True,
        "pattern": [".*clima actual.*", ".*datos del clima.*", ".*informacion del clima.*", ".*temperatura actual.*", ".*temperatura de.*", ".*estadisticas del clima.*"],
        "templates": ["{}"],
        "func": WeatherSkills.tell_the_weather,
        "tags": "clima actual,datos del clima,informacion del clima,temperatura actual,temperatura de,estadisticas del clima",
        "description": "Calculos",
        "context": "",
        "next": []
    },



]

"""{
        "enable": True,
        "pattern": [""],
        "templates": ["{}"],
        "func": MathSkills.do_calculations,
        "tags": math_tags,
        "description": "Calculos",
        "context": "",
        "next": []
    },"""


def get_skills():
    return BASIC_SKILLS + CONTROL_SKILLS
