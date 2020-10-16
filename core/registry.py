#!/usr/bin/env python3
from core.collections.activation import ActivationSkills
from core.collections.general import UtilSkills
from core.collections.datetime import DatetimeSkills
from core.collections.internet import InternetSkills
from core.collections.redimer import ReminderSkills
from core.collections.internet import InternetSkills
from core.collections.math import MathSkills
from core.collections.weather import WeatherSkills
from core.collections.alarm import AlarmSkills
from core.collections.music import MusicSkills
from core.collections.newspaper import NewsPaperSkills
from utils.mapping import math_tags

CONTROL_SKILLS = [
    {
        "func": ActivationSkills.assistant_greeting,
        "pattern": [".*buenos dias.*", ".*buenas tardes.*", ".*buenas noches.*"],
        "templates": ["{}"],
        "tags": "saludos iniciales",
        "description": "Comandos para activar el sistema",
        "context": "",
        "next": []
    },

    {
        "func": ActivationSkills.disable_assistant,
        "pattern": [".*deshabilitar asistente.*", ".*pausar asistente.*", ".*dejar de escuchar.*", ".*deja de escuchar.*", ".*dormir asistente.*", ".*dormir el asistente.*",
                    ".*desactivar asistente.*",  ".*desactivar el asistente.*"],
        "templates": ["{}"],
        "tags": "deshabilita el asistente",
        "description": "Poner el sistema en pausa",
        "context": "",
        "next": []
    },

    {
        "func": ActivationSkills.enable_assistant,
        "pattern": [".*habilitar asistente.*", ".*habilitar el asistente.*", ".*habilita el asistente.*", ".*reanudar asistente.*", ".*comenzar a escuchar.*", ".*despertar asistente.*",
                    ".*activar asistente.*", ".*activar el asistente.*"],
        "templates": ["{}"],
        "tags": "habilitar el asistente",
        "description": "Poner el sistema en pausa",
        "context": "",
        "next": []
    }
]

BASIC_SKILLS = [
    #hora
    {
        "enable": True,
        "pattern": [".*que hora es.*", ".*que hora.*", ".*hora actual.*"],
        "templates": ["{}", "la hora actual es {}", "son las {}"],
        "func": DatetimeSkills.tell_the_time,
        "tags": "hora actual",
        "description": "Dice la hora actual",
        "context": "datetime",
        "next": []
    },
    #fecha
    {
        "enable": True,
        "pattern": [".*fecha actual.*", ".*dia es hoy.*"],
        "templates": ["{}", "hoy es {}", "la fecha actual es {}"],
        "func": DatetimeSkills.tell_the_date,
        "tags": "fecha actual",
        "description": "Dice la fecha actual",
        "context": "datetime",
        "next": []
    },
    #volumen
    {
        "enable": True,
        "pattern": [".*detener ahora.*", ".*detener cancion.*", ".*detener audio.*", ".*detener sonido.*", ".*de tener ahora.*", ".*de tener cancion.*", ".*de tener audio.*", ".*de tener sonido.*", ".*parar ahora.*", ".*parar cancion.*", ".*parar audio.*", ".*parar sonido.*"],
        "templates": ["se detiene la reproduccion actual {}", "se detiene el sonido {}"],
        "func": UtilSkills.speech_interruption,
        "tags": "detener ahora",
        "description": "detiene la reproducción actual",
        "context": "volume",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*subir volumen.*", ".*subir el volumen.*", ".*incrementar volumen.*", ".*incrementar el volumen.*", ".*aumentar volumen.*", ".*aumentar el volumen.*", ".*elevar volumen.*", ".*elevar el volumen.*"],
        "templates": ["{}"],
        "func": UtilSkills.increase_master_volume,
        "tags": "subir volumen",
        "description": "Sube el volumen",
        "context": "volume",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*reducir volumen.*", ".*bajar volumen.*", ".*disminuir volumen.*", ".*decrementar volumen.*", ".*reducir el volumen.*", ".*bajar el volumen.*", ".*disminuir el volumen.*", ".*decrementar el volumen.*"],
        "templates": ["{}"],
        "func": UtilSkills.reduce_master_volume,
        "tags": "bajar volumen",
        "description": "Decrementa el volumen",
        "context": "volume",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*silenciar volumen.*", ".*bajar todo el volumen.*", ".*silencinar el volumen.*", ".*bajar todo volumen.*"],
        "templates": ["{}"],
        "func": UtilSkills.mute_master_volume,
        "tags": "silenciar volumen",
        "description": "Silencia el volumen",
        "context": "volume",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*volumen al maximo.*", ".*volumen total.*", ".*volumen al 100.*", ".*volumen maximo.*"],
        "templates": ["{}"],
        "func": UtilSkills.max_master_volume,
        "tags": "volumen al maximo",
        "description": "maximo volumen",
        "context": "volume",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*volumen actual.*", ".*volumen en este momento.*", ".*porcentaje de volumen.*", ".*porcentaje volumen.*"],
        "templates": ["{}"],
        "func": UtilSkills.current_master_volume,
        "tags": "volumen actual",
        "description": "Actual volumen",
        "context": "volume",
        "next": []
    },
    #internet
    {
        "enable": True,
        "pattern": [".*conexion a internet.*", ".*internet actual.*", ".*hay internet.*", ".*conexion internet.*", ".*revisar internet.*"],
        "templates": ["{}"],
        "func": InternetSkills.internet_availability,
        "tags": "conexion a internet",
        "description": "Revisar conexión a internet",
        "context": "internet",
        "next": []
    },
    #reminder

    {
        "enable": True,
        "pattern": [".*lista de recordatorios.*", ".*listas de recordatorios.*", ".*lista de recordatorio.*", ".*listas de recordatorio.*",
                    ".*listado de recordatorios.*", ".*listado de recordatorio.*",
                    ".*lista do de recordatorios.*", ".*lista do de recordatorio.*",
                    ".*listar los recordatorios.*", ".*listar los recordatorio.*",
                    ".*listame los recordatorios.*", ".*listame los recordatorio.*",
                    ".*lista me los recordatorios.*", ".*lista me los recordatorio.*",
                    ".*listarme los recordatorios.*", ".*listarme los recordatorio.*",
                    ".*listar me los recordatorios.*", ".*listar me los recordatorio.*"],
        "templates": ["{}"],
        "func": ReminderSkills.list_all,
        "tags": "listado de recordatorios",
        "description": "Recordatorio",
        "context": "reminder",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*detener los recordatorios.*", ".*detener todos (.*) recordatorios.*",
                    ".*parar los recordatorios.*", ".*parar todos (.*) recordatorios.*",
                    ".*eliminar los recordatorios.*", ".*eliminar todos (.*) recordatorios.*"],
        "templates": ["{}"],
        "func": ReminderSkills.stop_all,
        "tags": "detenet o eliminar recordatorios",
        "description": "Recordatorio",
        "context": "reminder",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*recuerdame (.*) en (.*) minutos", ".*recuerda me (.*) en (.*) mimutos", ".*recordarme (.*) en (.*) minutos", ".*recordar me (.*) en (.*) minutos",
                    ".*recuerdame (.*) en (.*) minuto", ".*recuerda me (.*) en (.*) mimuto", ".*recordarme (.*) en (.*) minuto", ".*recordar me (.*) en (.*) minuto"],
        "templates": ["{}"],
        "func": ReminderSkills.create_reminder_action_time_minutes,
        "tags": "recordatorio por accion y tiempo",
        "description": "Recordatorio",
        "context": "reminder",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*recuerdame en (.*) minutos (.*)", ".*recuerda me en (.*) minutos (.*)", ".*recordarme en (.*) minutos (.*)", ".*recordar me en (.*) minutos (.*)",
                    ".*recuerdame en (.*) minuto (.*)", ".*recuerda me en (.*) minuto (.*)", ".*recordarme en (.*) minuto (.*)", ".*recordar me en (.*) minuto (.*)"],
        "templates": ["{}"],
        "func": ReminderSkills.create_reminder_time_action_minutes,
        "tags": "recordatorio por tiempo y accion",
        "description": "Recordatorio",
        "context": "reminder",
        "next": []
    },

    {
        "enable": True,
        "pattern": [

                    ".*recuerdame a las (.*):(.*) p\.m\. (.*)", ".*recuerda me a las (.*):(.*) p\.m\. (.*)", ".*recordarme a las (.*):(.*) p\.m\. (.*)", ".*recordar me a las (.*):(.*) p\.m\. (.*)",
                    ".*recuerdame a las (.*):(.*)p\.m\.(.*)", ".*recuerda me a las (.*):(.*)p\.m\.(.*)", ".*recordarme a las (.*):(.*)p\.m\.(.*)", ".*recordar me a las (.*):(.*)p\.m\.(.*)",
                    ".*recuerdame a las (.*) y (.*) p\.m\. (.*)", ".*recuerda me a las (.*) y (.*)p\.m\. (.*)", ".*recordarme a las (.*) y (.*)p\.m\. (.*)", ".*recordar me a las (.*) y (.*)p\.m\. (.*)",
                    ".*recuerdame a las (.*)y(.*)p\.m\.(.*)", ".*recuerda me a las (.*)y(.*)p\.m\.(.*)", ".*recordarme a las (.*)y(.*)p\.m\.(.*)", ".*recordar me a las (.*)y(.*)p\.m\.(.*)",

                    ".*recuerdame a las (.*):(.*) p.m. (.*)", ".*recuerda me a las (.*):(.*) p.m. (.*)", ".*recordarme a las (.*):(.*) p.m. (.*)", ".*recordar me a las (.*):(.*) p.m. (.*)",
                    ".*recuerdame a las (.*):(.*)p.m.(.*)", ".*recuerda me a las (.*):(.*)p.m.(.*)", ".*recordarme a las (.*):(.*)p.m.(.*)", ".*recordar me a las (.*):(.*)p.m.(.*)",
                    ".*recuerdame a las (.*) y (.*) p.m. (.*)", ".*recuerda me a las (.*) y (.*)p.m. (.*)", ".*recordarme a las (.*) y (.*)p.m. (.*)", ".*recordar me a las (.*) y (.*)p.m. (.*)",
                    ".*recuerdame a las (.*)y(.*)p.m.(.*)", ".*recuerda me a las (.*)y(.*)p.m.(.*)", ".*recordarme a las (.*)y(.*)p.m.(.*)", ".*recordar me a las (.*)y(.*)p.m.(.*)",

                    ".*recuerdame a las (.*):(.*) pm (.*)", ".*recuerda me a las (.*):(.*) pm (.*)", ".*recordarme a las (.*):(.*) pm (.*)", ".*recordar me a las (.*):(.*) pm (.*)",
                    ".*recuerdame a las (.*):(.*)pm(.*)", ".*recuerda me a las (.*):(.*)pm(.*)", ".*recordarme a las (.*):(.*)pm(.*)", ".*recordar me a las (.*):(.*)pm(.*)",
                    ".*recuerdame a las (.*) y (.*) pm (.*)", ".*recuerda me a las (.*) y (.*) pm (.*)", ".*recordarme a las (.*) y (.*) pm (.*)", ".*recordar me a las (.*) y (.*) pm (.*)",
                    ".*recuerdame a las (.*)y(.*)pm(.*)", ".*recuerda me a las (.*)y(.*)pm(.*)", ".*recordarme a las (.*)y(.*)pm(.*)", ".*recordar me a las (.*)y(.*)pm(.*)",



                    ".*recuerdame a la (.*):(.*) p\.m\. (.*)", ".*recuerda me a la (.*):(.*) p\.m\. (.*)", ".*recordarme a la (.*):(.*) p\.m\. (.*)", ".*recordar me a la (.*):(.*) p\.m\. (.*)",
                    ".*recuerdame a la (.*):(.*)p\.m\.(.*)", ".*recuerda me a la (.*):(.*)p\.m\.(.*)", ".*recordarme a la (.*):(.*)p\.m\.(.*)", ".*recordar me a la (.*):(.*)p\.m\.(.*)",
                    ".*recuerdame a la (.*) y (.*) p\.m\. (.*)", ".*recuerda me a la (.*) y (.*)p\.m\. (.*)", ".*recordarme a la (.*) y (.*)p\.m\. (.*)", ".*recordar me a la (.*) y (.*)p\.m\. (.*)",
                    ".*recuerdame a la (.*)y(.*)p\.m\.(.*)", ".*recuerda me a la (.*)y(.*)p\.m\.(.*)", ".*recordarme a la (.*)y(.*)p\.m\.(.*)", ".*recordar me a la (.*)y(.*)p\.m\.(.*)",

                    ".*recuerdame a la (.*):(.*) p.m. (.*)", ".*recuerda me a la (.*):(.*) p.m. (.*)", ".*recordarme a la (.*):(.*) p.m. (.*)", ".*recordar me a la (.*):(.*) p.m. (.*)",
                    ".*recuerdame a la (.*):(.*)p.m.(.*)", ".*recuerda me a la (.*):(.*)p.m.(.*)", ".*recordarme a la (.*):(.*)p.m.(.*)", ".*recordar me a la (.*):(.*)p.m.(.*)",
                    ".*recuerdame a la (.*) y (.*) p.m. (.*)", ".*recuerda me a la (.*) y (.*)p.m. (.*)", ".*recordarme a la (.*) y (.*)p.m. (.*)", ".*recordar me a la (.*) y (.*)p.m. (.*)",
                    ".*recuerdame a la (.*)y(.*)p.m.(.*)", ".*recuerda me a la (.*)y(.*)p.m.(.*)", ".*recordarme a la (.*)y(.*)p.m.(.*)", ".*recordar me a la (.*)y(.*)p.m.(.*)",

                    ".*recuerdame a la (.*):(.*) pm (.*)", ".*recuerda me a la (.*):(.*) pm (.*)", ".*recordarme a la (.*):(.*) pm (.*)", ".*recordar me a la (.*):(.*) pm (.*)",
                    ".*recuerdame a la (.*):(.*)pm(.*)", ".*recuerda me a la (.*):(.*)pm(.*)", ".*recordarme a la (.*):(.*)pm(.*)", ".*recordar me a la (.*):(.*)pm(.*)",
                    ".*recuerdame a la (.*) y (.*) pm (.*)", ".*recuerda me a la (.*) y (.*) pm (.*)", ".*recordarme a la (.*) y (.*) pm (.*)", ".*recordar me a la (.*) y (.*) pm (.*)",
                    ".*recuerdame a la (.*)y(.*)pm(.*)", ".*recuerda me a la (.*)y(.*)pm(.*)", ".*recordarme a la (.*)y(.*)pm(.*)", ".*recordar me a la (.*)y(.*)pm(.*)"

                    ],
        "templates": ["{}"],
        "func": ReminderSkills.create_reminder_time_action_pm,
        "tags": "recordatorio por hora y accion pm",
        "description": "Recordatorio",
        "context": "reminder",
        "next": []
    },

    {
        "enable": True,
        "pattern": [
                    
                    ".*recuerdame (.*) a las (.*):(.*) p\.m\.", ".*recuerda me (.*) a las (.*):(.*) p\.m\.", ".*recordarme (.*) a las (.*):(.*) p\.m\.", ".*recordar me (.*) a las (.*):(.*) p\.m\.",
                    ".*recuerdame (.*)a las (.*):(.*)p\.m\.", ".*recuerda me (.*)a las (.*):(.*)p\.m\.", ".*recordarme (.*)a las (.*):(.*)p\.m\.", ".*recordar me (.*)a las (.*):(.*)p\.m\.",
                    ".*recuerdame (.*) a las (.*) y (.*) p\.m\.", ".*recuerda me (.*) a las (.*) y (.*) p\.m\.", ".*recordarme (.*) a las (.*) y (.*) p\.m\.", ".*recordar me (.*) a las (.*) y (.*) p\.m\.",
                    ".*recuerdame (.*)a las (.*)y(.*)p\.m\.", ".*recuerda me (.*)a las (.*)y(.*)p\.m\.", ".*recordarme (.*)a las (.*)y(.*)p\.m\.", ".*recordar me (.*)a las (.*)y(.*)p\.m\.",

                    ".*recuerdame (.*) a las (.*):(.*) p.m.", ".*recuerda me (.*) a las (.*):(.*) p.m.", ".*recordarme (.*) a las (.*):(.*) p.m.", ".*recordar me (.*) a las (.*):(.*) p.m.",
                    ".*recuerdame (.*)a las (.*):(.*)p.m.", ".*recuerda me (.*)a las (.*):(.*)p.m.", ".*recordarme (.*)a las (.*):(.*)p.m.", ".*recordar me (.*)a las (.*):(.*)p.m.",
                    ".*recuerdame (.*) a las (.*) y (.*) p.m.", ".*recuerda me (.*) a las (.*) y (.*) p.m.", ".*recordarme (.*) a las (.*) y (.*) p.m.", ".*recordar me (.*) a las (.*) y (.*) p.m.",
                    ".*recuerdame (.*)a las (.*)y(.*)p.m.", ".*recuerda me (.*)a las (.*)y(.*)p.m.", ".*recordarme (.*)a las (.*)y(.*)p.m.", ".*recordar me (.*)a las (.*)y(.*)p.m.",

                    ".*recuerdame (.*) a las (.*):(.*) pm", ".*recuerda me (.*) a las (.*):(.*) pm", ".*recordarme (.*) a las (.*):(.*) pm", ".*recordar me (.*) a las (.*):(.*) pm",
                    ".*recuerdame (.*)a las (.*):(.*)pm", ".*recuerda me (.*)a las (.*):(.*)pm", ".*recordarme (.*)a las (.*):(.*)pm", ".*recordar me (.*)a las (.*):(.*)pm",
                    ".*recuerdame (.*) a las (.*) y (.*) pm", ".*recuerda me (.*) a las (.*) y (.*) pm", ".*recordarme (.*) a las (.*) y (.*) pm", ".*recordar me (.*) a las (.*) y (.*) pm",
                    ".*recuerdame (.*)a las (.*)y(.*)pm", ".*recuerda me (.*)a las (.*)y(.*)pm", ".*recordarme (.*)a las (.*)y(.*)pm", ".*recordar me (.*)a las (.*)y(.*)pm",


                   
                    ".*recuerdame (.*) a la (.*):(.*) p\.m\.", ".*recuerda me (.*) a la (.*):(.*) p\.m\.", ".*recordarme (.*) a la (.*):(.*) p\.m\.", ".*recordar me (.*) a la (.*):(.*) p\.m\.",
                    ".*recuerdame (.*)a la (.*):(.*)p\.m\.", ".*recuerda me (.*)a la (.*):(.*)p\.m\.", ".*recordarme (.*)a la (.*):(.*)p\.m\.", ".*recordar me (.*)a la (.*):(.*)p\.m\.",
                    ".*recuerdame (.*) a la (.*) y (.*) p\.m\.", ".*recuerda me (.*) a la (.*) y (.*) p\.m\.", ".*recordarme (.*) a la (.*) y (.*) p\.m\.", ".*recordar me (.*) a la (.*) y (.*) p\.m\.",
                    ".*recuerdame (.*)a la (.*)y(.*)p\.m\.", ".*recuerda me (.*)a la (.*)y(.*)p\.m\.", ".*recordarme (.*)a la (.*)y(.*)p\.m\.", ".*recordar me (.*)a la (.*)y(.*)p\.m\.",

                    ".*recuerdame (.*) a la (.*):(.*) p.m.", ".*recuerda me (.*) a la (.*):(.*) p.m.", ".*recordarme (.*) a la (.*):(.*) p.m.", ".*recordar me (.*) a la (.*):(.*) p.m.",
                    ".*recuerdame (.*)a la (.*):(.*)p.m.", ".*recuerda me (.*)a la (.*):(.*)p.m.", ".*recordarme (.*)a la (.*):(.*)p.m.", ".*recordar me (.*)a la (.*):(.*)p.m.",
                    ".*recuerdame (.*) a la (.*) y (.*) p.m.", ".*recuerda me (.*) a la (.*) y (.*) p.m.", ".*recordarme (.*) a la (.*) y (.*) p.m.", ".*recordar me (.*) a la (.*) y (.*) p.m.",
                    ".*recuerdame (.*)a la (.*)y(.*)p.m.", ".*recuerda me (.*)a la (.*)y(.*)p.m.", ".*recordarme (.*)a la (.*)y(.*)p.m.", ".*recordar me (.*)a la (.*)y(.*)p.m.",

                    ".*recuerdame (.*) a la (.*):(.*) pm", ".*recuerda me (.*) a la (.*):(.*) pm", ".*recordarme (.*) a la (.*):(.*) pm", ".*recordar me (.*) a la (.*):(.*) pm",
                    ".*recuerdame (.*)a la (.*):(.*)pm", ".*recuerda me (.*)a la (.*):(.*)pm", ".*recordarme (.*)a la (.*):(.*)pm", ".*recordar me (.*)a la (.*):(.*)pm",
                    ".*recuerdame (.*) a la (.*) y (.*) pm", ".*recuerda me (.*) a la (.*) y (.*) pm", ".*recordarme (.*) a la (.*) y (.*) pm", ".*recordar me (.*) a la (.*) y (.*) pm",
                    ".*recuerdame (.*)a la (.*)y(.*)pm", ".*recuerda me (.*)a la (.*)y(.*)pm", ".*recordarme (.*)a la (.*)y(.*)pm", ".*recordar me (.*)a la (.*)y(.*)pm"
                    ],
        "templates": ["{}"],
        "func": ReminderSkills.create_reminder_action_time_pm,
        "tags": "recordatorio por accion y hora pm",
        "description": "Recordatorio",
        "context": "reminder",
        "next": []
    },

    {
        "enable": True,
        "pattern": [

                    ".*recuerdame a las (.*):(.*) a\.m\. (.*)", ".*recuerda me a las (.*):(.*) a\.m\. (.*)", ".*recordarme a las (.*):(.*) a\.m\. (.*)", ".*recordar me a las (.*):(.*) a\.m\. (.*)",
                    ".*recuerdame a las (.*):(.*)a\.m\.(.*)", ".*recuerda me a las (.*):(.*)a\.m\.(.*)", ".*recordarme a las (.*):(.*)a\.m\.(.*)", ".*recordar me a las (.*):(.*)a\.m\.(.*)",
                    ".*recuerdame a las (.*) y (.*) a\.m\. (.*)", ".*recuerda me a las (.*) y (.*)a\.m\. (.*)", ".*recordarme a las (.*) y (.*)a\.m\. (.*)", ".*recordar me a las (.*) y (.*)a\.m\. (.*)",
                    ".*recuerdame a las (.*)y(.*)a\.m\.(.*)", ".*recuerda me a las (.*)y(.*)a\.m\.(.*)", ".*recordarme a las (.*)y(.*)a\.m\.(.*)", ".*recordar me a las (.*)y(.*)a\.m\.(.*)",

                    ".*recuerdame a las (.*):(.*) a.m. (.*)", ".*recuerda me a las (.*):(.*) a.m. (.*)", ".*recordarme a las (.*):(.*) a.m. (.*)", ".*recordar me a las (.*):(.*) a.m. (.*)",
                    ".*recuerdame a las (.*):(.*)a.m.(.*)", ".*recuerda me a las (.*):(.*)a.m.(.*)", ".*recordarme a las (.*):(.*)a.m.(.*)", ".*recordar me a las (.*):(.*)a.m.(.*)",
                    ".*recuerdame a las (.*) y (.*) a.m. (.*)", ".*recuerda me a las (.*) y (.*)a.m. (.*)", ".*recordarme a las (.*) y (.*)a.m. (.*)", ".*recordar me a las (.*) y (.*)a.m. (.*)",
                    ".*recuerdame a las (.*)y(.*)a.m.(.*)", ".*recuerda me a las (.*)y(.*)a.m.(.*)", ".*recordarme a las (.*)y(.*)a.m.(.*)", ".*recordar me a las (.*)y(.*)a.m.(.*)",

                    ".*recuerdame a las (.*):(.*) am (.*)", ".*recuerda me a las (.*):(.*) am (.*)", ".*recordarme a las (.*):(.*) am (.*)", ".*recordar me a las (.*):(.*) am (.*)",
                    ".*recuerdame a las (.*):(.*)am(.*)", ".*recuerda me a las (.*):(.*)am(.*)", ".*recordarme a las (.*):(.*)am(.*)", ".*recordar me a las (.*):(.*)am(.*)",
                    ".*recuerdame a las (.*) y (.*) am (.*)", ".*recuerda me a las (.*) y (.*) am (.*)", ".*recordarme a las (.*) y (.*) am (.*)", ".*recordar me a las (.*) y (.*) am (.*)",
                    ".*recuerdame a las (.*)y(.*)am(.*)", ".*recuerda me a las (.*)y(.*)am(.*)", ".*recordarme a las (.*)y(.*)am(.*)", ".*recordar me a las (.*)y(.*)am(.*)",


                    ".*recuerdame a la (.*):(.*) a\.m\. (.*)", ".*recuerda me a la (.*):(.*) a\.m\. (.*)", ".*recordarme a la (.*):(.*) a\.m\. (.*)", ".*recordar me a la (.*):(.*) a\.m\. (.*)",
                    ".*recuerdame a la (.*):(.*)a\.m\.(.*)", ".*recuerda me a la (.*):(.*)a\.m\.(.*)", ".*recordarme a la (.*):(.*)a\.m\.(.*)", ".*recordar me a la (.*):(.*)a\.m\.(.*)",
                    ".*recuerdame a la (.*) y (.*) a\.m\. (.*)", ".*recuerda me a la (.*) y (.*)a\.m\. (.*)", ".*recordarme a la (.*) y (.*)a\.m\. (.*)", ".*recordar me a la (.*) y (.*)a\.m\. (.*)",
                    ".*recuerdame a la (.*)y(.*)a\.m\.(.*)", ".*recuerda me a la (.*)y(.*)a\.m\.(.*)", ".*recordarme a la (.*)y(.*)a\.m\.(.*)", ".*recordar me a la (.*)y(.*)a\.m\.(.*)",

                    ".*recuerdame a la (.*):(.*) a.m. (.*)", ".*recuerda me a la (.*):(.*) a.m. (.*)", ".*recordarme a la (.*):(.*) a.m. (.*)", ".*recordar me a la (.*):(.*) a.m. (.*)",
                    ".*recuerdame a la (.*):(.*)a.m.(.*)", ".*recuerda me a la (.*):(.*)a.m.(.*)", ".*recordarme a la (.*):(.*)a.m.(.*)", ".*recordar me a la (.*):(.*)a.m.(.*)",
                    ".*recuerdame a la (.*) y (.*) a.m. (.*)", ".*recuerda me a la (.*) y (.*)a.m. (.*)", ".*recordarme a la (.*) y (.*)a.m. (.*)", ".*recordar me a la (.*) y (.*)a.m. (.*)",
                    ".*recuerdame a la (.*)y(.*)a.m.(.*)", ".*recuerda me a la (.*)y(.*)a.m.(.*)", ".*recordarme a la (.*)y(.*)a.m.(.*)", ".*recordar me a la (.*)y(.*)a.m.(.*)",

                    ".*recuerdame a la (.*):(.*) am (.*)", ".*recuerda me a la (.*):(.*) am (.*)", ".*recordarme a la (.*):(.*) am (.*)", ".*recordar me a la (.*):(.*) am (.*)",
                    ".*recuerdame a la (.*):(.*)am(.*)", ".*recuerda me a la (.*):(.*)am(.*)", ".*recordarme a la (.*):(.*)am(.*)", ".*recordar me a la (.*):(.*)am(.*)",
                    ".*recuerdame a la (.*) y (.*) am (.*)", ".*recuerda me a la (.*) y (.*) am (.*)", ".*recordarme a la (.*) y (.*) am (.*)", ".*recordar me a la (.*) y (.*) am (.*)",
                    ".*recuerdame a la (.*)y(.*)am(.*)", ".*recuerda me a la (.*)y(.*)am(.*)", ".*recordarme a la (.*)y(.*)am(.*)", ".*recordar me a la (.*)y(.*)am(.*)"
                    ],
        "templates": ["{}"],
        "func": ReminderSkills.create_reminder_time_action_am,
        "tags": "recordatorio por hora y accion am",
        "description": "Recordatorio",
        "context": "reminder",
        "next": []
    },

    {
        "enable": True,
        "pattern": [
                    
                    ".*recuerdame (.*) a las (.*):(.*) a\.m\.", ".*recuerda me (.*) a las (.*):(.*) a\.m\.", ".*recordarme (.*) a las (.*):(.*) a\.m\.", ".*recordar me (.*) a las (.*):(.*) a\.m\.",
                    ".*recuerdame (.*)a las (.*):(.*)a\.m\.", ".*recuerda me (.*)a las (.*):(.*)a\.m\.", ".*recordarme (.*)a las (.*):(.*)a\.m\.", ".*recordar me (.*)a las (.*):(.*)a\.m\.",
                    ".*recuerdame (.*) a las (.*) y (.*) a\.m\.", ".*recuerda me (.*) a las (.*) y (.*) a\.m\.", ".*recordarme (.*) a las (.*) y (.*) a\.m\.", ".*recordar me (.*) a las (.*) y (.*) a\.m\.",
                    ".*recuerdame (.*)a las (.*)y(.*)a\.m\.", ".*recuerda me (.*)a las (.*)y(.*)a\.m\.", ".*recordarme (.*)a las (.*)y(.*)a\.m\.", ".*recordar me (.*)a las (.*)y(.*)a\.m\.",

                    ".*recuerdame (.*) a las (.*):(.*) a.m.", ".*recuerda me (.*) a las (.*):(.*) a.m.", ".*recordarme (.*) a las (.*):(.*) a.m.", ".*recordar me (.*) a las (.*):(.*) a.m.",
                    ".*recuerdame (.*)a las (.*):(.*)a.m.", ".*recuerda me (.*)a las (.*):(.*)a.m.", ".*recordarme (.*)a las (.*):(.*)a.m.", ".*recordar me (.*)a las (.*):(.*)a.m.",
                    ".*recuerdame (.*) a las (.*) y (.*) a.m.", ".*recuerda me (.*) a las (.*) y (.*) a.m.", ".*recordarme (.*) a las (.*) y (.*) a.m.", ".*recordar me (.*) a las (.*) y (.*) a.m.",
                    ".*recuerdame (.*)a las (.*)y(.*)a.m.", ".*recuerda me (.*)a las (.*)y(.*)a.m.", ".*recordarme (.*)a las (.*)y(.*)a.m.", ".*recordar me (.*)a las (.*)y(.*)a.m.",

                    ".*recuerdame (.*) a las (.*):(.*) am", ".*recuerda me (.*) a las (.*):(.*) am", ".*recordarme (.*) a las (.*):(.*) am", ".*recordar me (.*) a las (.*):(.*) am",
                    ".*recuerdame (.*)a las (.*):(.*)am", ".*recuerda me (.*)a las (.*):(.*)am", ".*recordarme (.*)a las (.*):(.*)am", ".*recordar me (.*)a las (.*):(.*)am",
                    ".*recuerdame (.*) a las (.*) y (.*) am", ".*recuerda me (.*) a las (.*) y (.*) am", ".*recordarme (.*) a las (.*) y (.*) am", ".*recordar me (.*) a las (.*) y (.*) am",
                    ".*recuerdame (.*)a las (.*)y(.*)am", ".*recuerda me (.*)a las (.*)y(.*)am", ".*recordarme (.*)a las (.*)y(.*)am", ".*recordar me (.*)a las (.*)y(.*)am",


                    
                    ".*recuerdame (.*) a la (.*):(.*) a\.m\.", ".*recuerda me (.*) a la (.*):(.*) a\.m\.", ".*recordarme (.*) a la (.*):(.*) a\.m\.", ".*recordar me (.*) a la (.*):(.*) a\.m\.",
                    ".*recuerdame (.*)a la (.*):(.*)a\.m\.", ".*recuerda me (.*)a la (.*):(.*)a\.m\.", ".*recordarme (.*)a la (.*):(.*)a\.m\.", ".*recordar me (.*)a la (.*):(.*)a\.m\.",
                    ".*recuerdame (.*) a la (.*) y (.*) a\.m\.", ".*recuerda me (.*) a la (.*) y (.*) a\.m\.", ".*recordarme (.*) a la (.*) y (.*) a\.m\.", ".*recordar me (.*) a la (.*) y (.*) a\.m\.",
                    ".*recuerdame (.*)a la (.*)y(.*)a\.m\.", ".*recuerda me (.*)a la (.*)y(.*)a\.m\.", ".*recordarme (.*)a la (.*)y(.*)a\.m\.", ".*recordar me (.*)a la (.*)y(.*)a\.m\.",

                    ".*recuerdame (.*) a la (.*):(.*) a.m.", ".*recuerda me (.*) a la (.*):(.*) a.m.", ".*recordarme (.*) a la (.*):(.*) a.m.", ".*recordar me (.*) a la (.*):(.*) a.m.",
                    ".*recuerdame (.*)a la (.*):(.*)a.m.", ".*recuerda me (.*)a la (.*):(.*)a.m.", ".*recordarme (.*)a la (.*):(.*)a.m.", ".*recordar me (.*)a la (.*):(.*)a.m.",
                    ".*recuerdame (.*) a la (.*) y (.*) a.m.", ".*recuerda me (.*) a la (.*) y (.*) a.m.", ".*recordarme (.*) a la (.*) y (.*) a.m.", ".*recordar me (.*) a la (.*) y (.*) a.m.",
                    ".*recuerdame (.*)a la (.*)y(.*)a.m.", ".*recuerda me (.*)a la (.*)y(.*)a.m.", ".*recordarme (.*)a la (.*)y(.*)a.m.", ".*recordar me (.*)a la (.*)y(.*)a.m.",

                    ".*recuerdame (.*) a la (.*):(.*) am", ".*recuerda me (.*) a la (.*):(.*) am", ".*recordarme (.*) a la (.*):(.*) am", ".*recordar me (.*) a la (.*):(.*) am",
                    ".*recuerdame (.*)a la (.*):(.*)am", ".*recuerda me (.*)a la (.*):(.*)am", ".*recordarme (.*)a la (.*):(.*)am", ".*recordar me (.*)a la (.*):(.*)am",
                    ".*recuerdame (.*) a la (.*) y (.*) am", ".*recuerda me (.*) a la (.*) y (.*) am", ".*recordarme (.*) a la (.*) y (.*) am", ".*recordar me (.*) a la (.*) y (.*) am",
                    ".*recuerdame (.*)a la (.*)y(.*)am", ".*recuerda me (.*)a la (.*)y(.*)am", ".*recordarme (.*)a la (.*)y(.*)am", ".*recordar me (.*)a la (.*)y(.*)am"
                    ],
        "templates": ["{}"],
        "func": ReminderSkills.create_reminder_action_time_am,
        "tags": "recordatorio por accion y hora am",
        "description": "Recordatorio",
        "context": "reminder",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*recuerdame (.*) en (.*) horas", ".*recuerda me (.*) en (.*) mimutos", ".*recordarme (.*) en (.*) horas", ".*recordar me (.*) en (.*) horas",
                    ".*recuerdame (.*) en (.*) hora", ".*recuerda me (.*) en (.*) mimuto", ".*recordarme (.*) en (.*) hora", ".*recordar me (.*) en (.*) hora"],
        "templates": ["{}"],
        "func": ReminderSkills.create_reminder_action_time_hours,
        "tags": "recordatorio accion y tiempo hora",
        "description": "Recordatorio",
        "context": "reminder",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*recuerdame en (.*) horas (.*)", ".*recuerda me en (.*) horas (.*)", ".*recordarme en (.*) horas (.*)", ".*recordar me en (.*) horas (.*)",
                    ".*recuerdame en (.*) hora (.*)", ".*recuerda me en (.*) hora (.*)", ".*recordarme en (.*) hora (.*)", ".*recordar me en (.*) hora (.*)"],
        "templates": ["{}"],
        "func": ReminderSkills.create_reminder_time_action_hours,
        "tags": "recordatorio tiempo y accion hora",
        "description": "Recordatorio",
        "context": "reminder",
        "next": []
    },
    # agregar recordatorio por accion, fecha y tiempo
    # alarma

    {
        "enable": True,
        "pattern": [".*lista de alarmas.*", ".*listas de alarmas.*", ".*lista de alarma.*", ".*listas de alarma.*",
                    ".*listado de alarmas.*", ".*listado de alarma.*",
                    ".*lista do de alarmas.*", ".*lista do de alarma.*",
                    ".*listar las alarmas.*", ".*listar las alarmas.*",
                    ".*listame las alarmas.*", ".*listame las alarma.*",
                    ".*lista me las alarmas.*", ".*lista me las alarma.*",
                    ".*listarme las alarmas.*", ".*listarme las alarma.*",
                    ".*listar me las alarmas.*", ".*listar me las alarma.*"],
        "templates": ["{}"],
        "func": AlarmSkills.list_all,
        "tags": "listado de alarmas",
        "description": "Recordatorio",
        "context": "alarm",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*detener las alarmas.*", ".*detener todas (.*) alarmas.*",
                    ".*parar las alarmas.*", ".*parar todas (.*) alarmas.*",
                    ".*eliminar las alarmas.*", ".*eliminar todas (.*) alarmas.*"],
        "templates": ["{}"],
        "func": AlarmSkills.stop_all,
        "tags": "detener o eliminar alarmas",
        "description": "Recordatorio",
        "context": "alarm",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*crear alarma en (.*) minutos", ".*crear alarma en (.*) minuto",
                    ".*establecer alarma en (.*) minutos", ".*establecer alarma en (.*) minuto",
                    ".*colocar alarma en (.*) minutos", ".*colocar alarma en (.*) minuto",
                    ".*agregar alarma en (.*) minutos", ".*agregar alarma en (.*) minuto"
                ],
        "templates": ["{}"],
        "func": AlarmSkills.create_alarm_time_minutes,
        "tags": "alarma por minutos",
        "description": "Recordatorio",
        "context": "alarm",
        "next": []
    },

    {
        "enable": True,
        "pattern": [".*crear alarma en (.*) hora", ".*crear alarma en (.*) hora",
                    ".*establecer alarma en (.*) hora", ".*establecer alarma en (.*) hora",
                    ".*colocar alarma en (.*) hora", ".*colocar alarma en (.*) hora",
                    ".*agregar alarma en (.*) hora", ".*agregar alarma en (.*) hora",

                    ".*crear alarma en (.*) horas", ".*crear alarma en (.*) horas",
                    ".*establecer alarma en (.*) horas", ".*establecer alarma en (.*) horas",
                    ".*colocar alarma en (.*) horas", ".*colocar alarma en (.*) horas",
                    ".*agregar alarma en (.*) horas", ".*agregar alarma en (.*) horas"
                ],
        "templates": ["{}"],
        "func": AlarmSkills.create_alarm_time_hours,
        "tags": "alarma por horas",
        "description": "Recordatorio",
        "context": "alarm",
        "next": []
    },


    {
        "enable": True,
        "pattern": [".*crear alarma a las (.*):(.*) a\.m\. de (.*) a (.*)",
                    ".*establecer alarma a las (.*):(.*) a\.m\. de (.*) a (.*)",
                    ".*colocar alarma a las (.*):(.*) a\.m\. de (.*) a (.*)",
                    ".*agregar alarma a las (.*):(.*) a\.m\. de (.*) a (.*)",

                    ".*crear alarma a la (.*):(.*) a\.m\. de (.*) a (.*)",
                    ".*establecer alarma a la (.*):(.*) a\.m\. de (.*) a (.*)",
                    ".*colocar alarma a la (.*):(.*) a\.m\. de (.*) a (.*)",
                    ".*agregar alarma a la (.*):(.*) a\.m\. de (.*) a (.*)",

                    ".*crear alarma a las (.*):(.*) a.*m.* de (.*) a (.*)",
                    ".*establecer alarma a las (.*):(.*) a.*m.* de (.*) a (.*)",
                    ".*colocar alarma a las (.*):(.*) a.*m.* de (.*) a (.*)",
                    ".*agregar alarma a las (.*):(.*) a.*m.* de (.*) a (.*)",

                    ".*crear alarma a la (.*):(.*) a.*m.* de (.*) a (.*)",
                    ".*establecer alarma a la (.*):(.*) a.*m.* de (.*) a (.*)",
                    ".*colocar alarma a la (.*):(.*) a.*m.* de (.*) a (.*)",
                    ".*agregar alarma a la (.*):(.*) a.*m.* de (.*) a (.*)"
                ],
        "templates": ["{}"],
        "func": AlarmSkills.create_alarm_range_time_week_am,
        "tags": "alarma por horas",
        "description": "Recordatorio",
        "context": "alarm",
        "next": []
    },


    {
        "enable": True,
        "pattern": [".*crear alarma de (.*) a (.*) a las (.*):(.*) a\.m\.",
                    ".*establecer alarma de (.*) a (.*) a las (.*):(.*) a\.m\.",
                    ".*colocar alarma de (.*) a (.*) a las (.*):(.*) a\.m\.",
                    ".*agregar alarma de (.*) a (.*) a las (.*):(.*) a\.m\.",

                    ".*crear alarma de (.*) a (.*) a la (.*):(.*) a\.m\.",
                    ".*establecer alarma de (.*) a (.*) a la (.*):(.*) a\.m\.",
                    ".*colocar alarma de (.*) a (.*) a la (.*):(.*) a\.m\.",
                    ".*agregar alarma de (.*) a (.*) a la (.*):(.*) a\.m\.",

                    ".*crear alarma de (.*) a (.*) a las (.*):(.*) a.*m.*",
                    ".*establecer alarma de (.*) a (.*) a las (.*):(.*) a.*m.*",
                    ".*colocar alarma de (.*) a (.*) a las (.*):(.*) a.*m.*",
                    ".*agregar alarma de (.*) a (.*) a las (.*):(.*) a.*m.*",

                    ".*crear alarma de (.*) a (.*) a la (.*):(.*) a.*m.*",
                    ".*establecer alarma de (.*) a (.*) a la (.*):(.*) a.*m.*",
                    ".*colocar alarma de (.*) a (.*) a la (.*):(.*) a.*m.*",
                    ".*agregar alarma de (.*) a (.*) a la (.*):(.*) a.*m.*"
                ],
        "templates": ["{}"],
        "func": AlarmSkills.create_alarm_range_week_time_am,
        "tags": "alarma por horas",
        "description": "Recordatorio",
        "context": "alarm",
        "next": []
    },


    {
        "enable": True,
        "pattern": [".*crear alarma a las (.*):(.*) p\.m\. de (.*) a (.*)",
                    ".*establecer alarma a las (.*):(.*) p\.m\. de (.*) a (.*)",
                    ".*colocar alarma a las (.*):(.*) p\.m\. de (.*) a (.*)",
                    ".*agregar alarma a las (.*):(.*) p\.m\. de (.*) a (.*)",

                    ".*crear alarma a la (.*):(.*) p\.m\. de (.*) a (.*)",
                    ".*establecer alarma a la (.*):(.*) p\.m\. de (.*) a (.*)",
                    ".*colocar alarma a la (.*):(.*) p\.m\. de (.*) a (.*)",
                    ".*agregar alarma a la (.*):(.*) p\.m\. de (.*) a (.*)",

                    ".*crear alarma a las (.*):(.*) p.*m.* de (.*) a (.*)",
                    ".*establecer alarma a las (.*):(.*) p.*m.* de (.*) a (.*)",
                    ".*colocar alarma a las (.*):(.*) p.*m.* de (.*) a (.*)",
                    ".*agregar alarma a las (.*):(.*) p.*m.* de (.*) a (.*)",

                    ".*crear alarma a la (.*):(.*) p.*m.* de (.*) a (.*)",
                    ".*establecer alarma a la (.*):(.*) p.*m.* de (.*) a (.*)",
                    ".*colocar alarma a la (.*):(.*) p.*m.* de (.*) a (.*)",
                    ".*agregar alarma a la (.*):(.*) p.*m.* de (.*) a (.*)"
                ],
        "templates": ["{}"],
        "func": AlarmSkills.create_alarm_range_time_week_pm,
        "tags": "alarma por horas",
        "description": "Recordatorio",
        "context": "alarm",
        "next": []
    },


    {
        "enable": True,
        "pattern": [".*crear alarma de (.*) a (.*) a las (.*):(.*) p\.m\.",
                    ".*establecer alarma de (.*) a (.*) a las (.*):(.*) p\.m\.",
                    ".*colocar alarma de (.*) a (.*) a las (.*):(.*) p\.m\.",
                    ".*agregar alarma de (.*) a (.*) a las (.*):(.*) p\.m\.",

                    ".*crear alarma de (.*) a (.*) a la (.*):(.*) p\.m\.",
                    ".*establecer alarma de (.*) a (.*) a la (.*):(.*) p\.m\.",
                    ".*colocar alarma de (.*) a (.*) a la (.*):(.*) p\.m\.",
                    ".*agregar alarma de (.*) a (.*) a la (.*):(.*) p\.m\.",

                    ".*crear alarma de (.*) a (.*) a las (.*):(.*) p.*m.*",
                    ".*establecer alarma de (.*) a (.*) a las (.*):(.*) p.*m.*",
                    ".*colocar alarma de (.*) a (.*) a las (.*):(.*) p.*m.*",
                    ".*agregar alarma de (.*) a (.*) a las (.*):(.*) p.*m.*",

                    ".*crear alarma de (.*) a (.*) a la (.*):(.*) p.*m.*",
                    ".*establecer alarma de (.*) a (.*) a la (.*):(.*) p.*m.*",
                    ".*colocar alarma de (.*) a (.*) a la (.*):(.*) p.*m.*",
                    ".*agregar alarma de (.*) a (.*) a la (.*):(.*) p.*m.*"
                ],
        "templates": ["{}"],
        "func": AlarmSkills.create_alarm_range_week_time_pm,
        "tags": "alarma por horas",
        "description": "Recordatorio",
        "context": "alarm",
        "next": []
    },
    # estado del tiempo
    {
        "enable": True,
        "pattern": [
            ".*clima en (.*)", ".*datos del clima en (.*)", ".*informacion del clima en (.*)", ".*temperatura actual en (.*)", ".*temperatura de (.*)", ".*estadisticas del clima.*", ".*estado del clima en (.*)",
            ".*clima en la ciudad de (.*)", ".*clima de la ciudad de (.*)"],
        "templates": ["{}"],
        "func": WeatherSkills.tell_the_weather,
        "tags": "clima actual,datos del clima,informacion del clima,temperatura actual,temperatura de,estadisticas del clima",
        "description": "Calculos",
        "context": "",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*clima actual.*", ".*datos del clima.*", ".*informacion del clima.*", ".*temperatura actual.*", ".*temperatura de.*", ".*estadisticas del clima.*", ".*estado del clima.*"],
        "templates": ["{}"],
        "func": WeatherSkills.tell_the_weather,
        "tags": "clima actual,datos del clima,informacion del clima,temperatura actual,temperatura de,estadisticas del clima",
        "description": "Calculos",
        "context": "",
        "next": []
    },
    #music
    {
        "enable": True,
        "pattern": [".*pon musica.*", ".*reproducir musica.*", ".*colocar musica.*", ".*pon cancion.*", ".*reproducir cancion.*", ".*colocar cancion.*"],
        "templates": ["{}"],
        "func": MusicSkills.play,
        "tags": "reproducir musica",
        "description": "Calculos",
        "context": "music",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*detener musica.*", ".*parar musica.*", ".*detener cancion.*", ".*parar cancion.*"],
        "templates": ["{}"],
        "func": MusicSkills.stop,
        "tags": "reproducir musica",
        "description": "Calculos",
        "context": "music",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*siguiente musica.*", ".*siguiente musica.*", ".*siguiente cancion.*", ".*siguiente cancion.*", ".*cambiar cancion.*", ".*cambiar musica.*"],
        "templates": ["{}"],
        "func": MusicSkills.next,
        "tags": "reproducir musica",
        "description": "Calculos",
        "context": "music",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*anterior musica.*", ".*anterior musica.*", ".*anterior cancion.*", ".*anterior cancion.*"],
        "templates": ["{}"],
        "func": MusicSkills.prev,
        "tags": "reproducir musica",
        "description": "Calculos",
        "context": "music",
        "next": []
    },
    #NewsPaperSkills
    {
        "enable": True,
        "pattern": [".*noticias actuales.*", ".*noticias de hoy.*", ".*noticias del dia.*",
                    ".*titulares actuales.*", ".*titulares de hoy.*", ".*titulares del dia.*"],
        "templates": ["{}"],
        "func": NewsPaperSkills.get_news,
        "tags": "noticias de hoy",
        "description": "",
        "context": "news",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*detener noticias.*", ".*parar noticias.*",".*detener las noticias.*", ".*parar las noticias.*", 
                    ".*detener titulares.*", ".*parar titulares.*",".*detener los titulares.*", ".*parar los titulares.*"],
        "templates": ["{}"],
        "func": NewsPaperSkills.stop,
        "tags": "detener noticias",
        "description": "",
        "context": "news",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*siguiente noticia.*", ".*siguiente noticias.*",".*cambiar noticias.*", ".*cambiar las noticias.*", 
                    ".*siguiente titular.*", ".*siguiente titulares.*",".*cambiar titular.*", ".*cambiar las titulares.*"],
        "templates": ["{}"],
        "func": NewsPaperSkills.next,
        "tags": "siguiente noticia",
        "description": "",
        "context": "news",
        "next": []
    },
    {
        "enable": True,
        "pattern": [".*anterior noticia.*", ".*anterior noticia.*", ".*anterior titular.*", ".*anterior titular.*"],
        "templates": ["{}"],
        "func": NewsPaperSkills.prev,
        "tags": "anterior titular",
        "description": "",
        "context": "news",
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
