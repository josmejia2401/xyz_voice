#!/usr/bin/env python3
from core.skill import AssistantSkill
import urllib.request as urllib2

class InternetSkills(AssistantSkill):

    @classmethod
    def _check_internet_connection(cls,**kwargs):
        try:
            urllib2.urlopen('http://www.google.com', timeout=1)
            return True
        except urllib2.URLError as err: 
            print(err)
            return False

    @classmethod
    def internet_availability(cls, ext = None, template = None, values = None, history = []):
        if cls.get_activation() == False:
            return
        if cls._check_internet_connection():
            r = template.format("Hay conexión a internet")
            cls.response(r)
        else:
            r = template.format("En este momento no hay conexión a internet")
            cls.response(r)