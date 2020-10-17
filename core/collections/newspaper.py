#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from core.skill import AssistantSkill
import threading
import time


class NewsThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            cont = 0
            while cont < len(NewsPaperSkills.txtfiles):
                time.sleep(0.8)
                if NewsPaperSkills.get_stop_speaking() == True:
                    NewsPaperSkills.set_stop_speaking(False)
                    break
                elif NewsPaperSkills.PREV == True:
                    NewsPaperSkills.PREV = False
                    if cont > 0:
                        cont = cont - 1
                    else:
                        cont = 0
                NewsPaperSkills.set_stop_speaking(False)
                x = NewsPaperSkills.txtfiles[cont]
                NewsPaperSkills.response(x)
                if NewsPaperSkills.PREV == False:
                    cont += 1
            print("HILO DE NEWS FINALIZADO")
        except Exception as e:
            print("NewsThread", e)

class NewsPaperSkills(AssistantSkill):
    txtfiles = []
    PREV = False
    THREAD_M = None

    @classmethod
    def get_news(cls, ext = None, template = None, values = None, history = []):
        try:
            if cls.get_activation() == False:
                return
            
            NewsPaperSkills.PREV = False
            NewsPaperSkills.txtfiles = []
            NewsPaperSkills.txtfiles.append("Del Espectador:")
            NewsPaperSkills.txtfiles = NewsPaperSkills.txtfiles + cls._get_el_espectador()

            NewsPaperSkills.txtfiles.append("De Blu radio:")
            NewsPaperSkills.txtfiles = NewsPaperSkills.txtfiles + cls._get_bluradio()

            NewsPaperSkills.THREAD_M = NewsThread()
            NewsPaperSkills.THREAD_M.start()

        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)

    @classmethod
    def next(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return
            NewsPaperSkills.PREV = False
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
            NewsPaperSkills.PREV = True
            cls.set_stop_speaking(True)
            cls.set_stop_speaking(False)
        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)

    @classmethod
    def _get_el_espectador(cls):
        r1 = requests.get('https://www.elespectador.com/')
        coverpage = r1.content
        soup1 = BeautifulSoup(coverpage, 'html5lib')
        t1 = soup1.find_all('h1', class_='Card_CustomLabel')
        span = soup1.find_all('span', class_='Card_CustomLabel')
        all_newspapers = t1 + span
        r = []
        for index, item in enumerate(all_newspapers):
            if index > 3:
                break
            r.append(item.get_text().strip())
        return r

    @classmethod
    def _get_bluradio(cls):
        r1 = requests.get('https://www.bluradio.com/')
        coverpage = r1.content
        soup1 = BeautifulSoup(coverpage, 'html5lib')
        #t1 = soup1.find_all('a', class_='Link')
        span = soup1.find_all('h3', class_='PromoA-title')
        all_newspapers = span
        r = []
        for index, item in enumerate(all_newspapers):
            if index > 3:
                break
            r.append(item.get_text().strip())
        return r

if __name__ == '__main__':
    get_bluradio()