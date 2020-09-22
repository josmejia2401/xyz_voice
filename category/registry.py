from category.collections.activation import ActivationSkills
from category.collections.general import UtilSkills
from category.collections.datetime import DatetimeSkills
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
        "tags": "iniciar, hola, iniciar sistema, buenas tardes, buenos días, buenas noches",
        "description": "Comandos para activar el sistema"
    },

    {
        "func": ActivationSkills.disable_assistant,
        "tags": "adiós, deshabilitar sistema, pausar sistema, apagar sistema, dejar de escuchar, dormir",
        "description": "Poner el sistema en pausa"
    }
]

BASIC_SKILLS = [
    {
        "enable": True,
        "func": DatetimeSkills.tell_the_time,
        "tags": "hora, que hora es, hora actual",
        "description": "Dice la hora actual"
    },

    {
        "enable": True,
        "func": DatetimeSkills.tell_the_date,
        "tags": "fecha, fecha actual, que dia es hoy",
        "description": "Dice la fecha actual"
    },
    {
        "enable": True,
        "func": UtilSkills.speech_interruption,
        "tags": "detener ahora, detener",
        "description": "detiene la reproducción actual"
    },
    {
        "enable": True,
        "func": UtilSkills.increase_master_volume,
        "tags": "subir volumen, incrementar volumen",
        "description": "Sube el volumen"
    },

    {
        "enable": True,
        "func": UtilSkills.reduce_master_volume,
        "tags": "bajar volumen, disminuir volumen",
        "description": "Decrementa el volumen"
    },

    {
        "enable": True,
        "func": UtilSkills.mute_master_volume,
        "tags": "silenciar volumen, bajar todo el volumen",
        "description": "Silencia el volumen"
    },

    {
        "enable": True,
        "func": UtilSkills.max_master_volume,
        "tags": "subir volumen al maximo, volumen al maximo, maximo volumen",
        "description": "maximo volumen"
    },
]




def get_func_from_skills(text):
    try:
        #text = " ".join(text)
        text = " ".join(e.strip() for e in text)
        for skill in BASIC_SKILLS + CONTROL_SKILLS:
            new_skills = skill["tags"].split(",")
            for sk in new_skills:
                if sk.strip() in text.strip():
                    func = skill["func"]
                    func()
                    return func
    except Exception as e:
        print(e)
    return None