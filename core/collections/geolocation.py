#!/usr/bin/env python3
import requests
from core.skill import AssistantSkill
from utils.settings import IPSTACK_API

class GeoLocationSkills(AssistantSkill):

    @classmethod
    def get_location(cls, ext = None, template = None, values = None, history = []):
        try:
            if cls.get_activation() == False:
                return
            location = cls._get_location()
            r = template.format('La ubicación es {}'.format(location))
            cls.response(r)
        except Exception as e:
            print(e)
            r = template.format('No se pudo procesar el comando')
            cls.response(r)

    @classmethod
    def _get_location(cls):
        if IPSTACK_API['KEY']:
            key = IPSTACK_API['KEY']
            url = IPSTACK_API['URL']
            r1 = requests.get(url.format(key))
            if r1.status_code == 200:
                result = r1.json()
                country_name = result['country_name']
                region_name = result['region_name']
                city = result['city']
                return city
            return None
        else:
            raise Exception('Ingrese la llave')
