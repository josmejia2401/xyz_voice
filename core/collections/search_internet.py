#!/usr/bin/env python3
from core.skill import AssistantSkill
from utils.search_internet import SearchInternet

class SearchInternetSkills(AssistantSkill):

    @classmethod
    def actual_temperature(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return
            if values:
                s = values[0]
                if isinstance(s, list):
                    s = s[0]
                elif isinstance(s, tuple):
                    s = s[0]
            else:
                s = "temperatura actual"
            soup = SearchInternet.search_google(s)
            result = SearchInternet.get_weather_states(soup)
            if result:
                x = "probabilidades en precipitaciones del {}, humedad de {} y viento de {}".format(result["probabilities"], result["humidity"], result["wind"])
                cls.response("la temperatura actual en {} es de {} {} con cielo {}. {}".format(result["place"], result["temperature"], result["degrees"], result["weather"], x))
            else:
                cls.response("No nay resultados en la busqueda")
        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)

    @classmethod
    def definition_word(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return
            s = values[0]
            if isinstance(s, list):
                s = s[0]
            elif isinstance(s, tuple):
                s = s[0]
            s = 'que es ' + s
            soup = SearchInternet.search_google(s)
            result = SearchInternet.get_definition(soup)
            if result:
                cls.response("género {}. definición: {}".format(result["gender"], result["definition"]))
            else:
                cls.response("No nay resultados en la busqueda")
        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)
        
    @classmethod
    def football_status(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return
            s = values[0]
            if isinstance(s, list):
                s = s[0]
            elif isinstance(s, tuple):
                s = s[0]
            print(s)
            soup = SearchInternet.search_google(s)
            result = SearchInternet.get_football(soup)
            if result:
                cls.response("{} {}, {} {}".format(result["local"], result["local_r"], result["visitor"], result["visitor_r"]))
            else:
                cls.response("No nay resultados en la busqueda")
        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)

    @classmethod
    def translate(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return
            q = values[0]
            if isinstance(q, list):
                s = q[0]
                de = q[1]
                a = q[1]
            elif isinstance(q, tuple):
                s = q[0]
                de = q[1]
                a = q[1]
            else:
                s = values[0]
                de = values[1]
                a = values[1]                
            print(s)
            soup = SearchInternet.search_translate(de, a, s)
            result = SearchInternet.get_translate(soup)
            if result:
                cls.response("{}".format(result["translate"]))
            else:
                cls.response("No nay resultados en la busqueda")
        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)