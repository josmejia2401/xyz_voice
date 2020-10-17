#!/usr/bin/env python3
from datetime import datetime
from core.skill import AssistantSkill
import os, fnmatch, threading
import requests
import bs4

class WikiThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            cont = 0
            while cont < len(WikiSkills.txtfiles):
                print("WikiSkills.get_stop_speaking()", WikiSkills.get_stop_speaking())
                if WikiSkills.get_stop_speaking() == True:
                    WikiSkills.set_stop_speaking(False)
                    break
                elif WikiSkills.PREV == True:
                    WikiSkills.PREV = False
                    if cont > 0:
                        cont = cont - 1
                    else:
                        cont = 0       
                x = WikiSkills.txtfiles[cont]
                WikiSkills.response(x)
                if WikiSkills.PREV == False:
                    cont += 1
            print("HILO DE WIKI FINALIZADO")
        except Exception as e:
            print("WikiThread", e)

class WikiSkills(AssistantSkill):

    txtfiles = []
    STOP = False
    PREV = False
    THREAD_M = None

    @classmethod
    def _get_wiki(cls, keyword):
        res = requests.get('https://es.wikipedia.org/wiki/' + str(keyword))
        res.raise_for_status()
        wiki = bs4.BeautifulSoup(res.text,"lxml")
        elems = wiki.select('p')
        WikiSkills.txtfiles = []
        cont = 0
        for i, item in enumerate(elems):
            if item.getText().strip():
                if cont > 2:
                    break
                WikiSkills.txtfiles.append(item.getText().strip())
                cont += 1

    @classmethod
    def play(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return
            WikiSkills.STOP = False
            WikiSkills.PREV = False
            KEYWORD = values[0]
            if isinstance(KEYWORD, list):
                KEYWORD = KEYWORD[0]
            elif isinstance(KEYWORD, tuple):
                KEYWORD = KEYWORD[0]
            cls._get_wiki(KEYWORD)
            if len(WikiSkills.txtfiles) > 0:
                WikiSkills.THREAD_M = WikiThread()
                WikiSkills.THREAD_M.start()
            else:
                cls.response("No nay resultados en la busqueda")
        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)

    @classmethod
    def next(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return
            WikiSkills.STOP = False
            WikiSkills.PREV = False
            cls.set_stop_speaking(True)
            cls.set_stop_speaking(False)
        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)

    
    @classmethod
    def prev(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return
            WikiSkills.STOP = False
            WikiSkills.PREV = True
            cls.set_stop_speaking(True)
            cls.set_stop_speaking(False)
        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)