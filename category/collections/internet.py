import requests
import logging
from category.skill import AssistantSkill
import urllib.request as urllib2

class InternetSkills(AssistantSkill):

    def check_internet_connection(cls):
        try:
            urllib2.urlopen('http://www.google.com', timeout=1)
            return True
        except urllib2.URLError as err: 
            return False

    @classmethod
    def internet_availability(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        Tells to the user is the internet is available or not.
        """
        if cls.check_internet_connection():
            cls.response("Hay conexión a internet")
            return True
        else:
            cls.response("En este momento no hay conexión a internet")
            return False