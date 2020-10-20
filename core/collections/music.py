#!/usr/bin/env python3
import sys
from datetime import datetime
from core.skill import AssistantSkill
from utils.dir import get_ouput_music
import os, fnmatch, threading

def find_mp3(pattern, path):
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

class MusicThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        try:
            cont = 0
            while cont < len(MusicSkills.txtfiles):
                if MusicSkills.get_stop_speaking() == True:
                    MusicSkills.set_stop_speaking(False)
                    break
                elif MusicSkills.PREV == True:
                    MusicSkills.PREV = False
                    if cont > 0:
                        cont = cont - 1
                    else:
                        cont = 0
                MusicSkills.set_stop_speaking(False)
                f = MusicSkills.txtfiles[cont]
                x = os.path.join(MusicSkills.DIR_MUSIC, f)
                MusicSkills.play_sound(x, False)
                if MusicSkills.PREV == False:
                    cont += 1
            print("HILO DE MUSICA FINALIZADO")
        except Exception as e:
            print("MusicThread", e)

class MusicSkills(AssistantSkill):

    DIR_MUSIC = get_ouput_music()
    txtfiles = []
    PREV = False
    THREAD_M = None

    @classmethod
    def _get_list_music(cls):
        # arr_txt = [x for x in os.listdir() if x.endswith(".txt")]
        # print(arr_txt)
        if len(MusicSkills.txtfiles) > 0:
            return
        f = MusicSkills.DIR_MUSIC
        MusicSkills.txtfiles = find_mp3('*.mp3', f)

    @classmethod
    def _reload_list_music(cls):
        MusicSkills.txtfiles = []
        cls._get_list_music()

    @classmethod
    def play(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return
            MusicSkills.PREV = False
            cls._reload_list_music()
            cls._get_list_music()
            MusicSkills.THREAD_M = MusicThread()
            MusicSkills.THREAD_M.start()
        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)

    @classmethod
    def next(cls, ext = None, template = None, values = None, history = []) -> None:
        try:
            if cls.get_activation() == False:
                return
            MusicSkills.PREV = False
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
            MusicSkills.PREV = True
            cls.set_stop_speaking(True)
            cls.set_stop_speaking(False)
        except Exception as e:
            print(e)
            r = template.format("No se pudo procesar el comando")
            cls.response(r)