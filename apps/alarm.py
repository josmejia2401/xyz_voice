#!/usr/bin/env python3
import datetime
import time
import os
import threading
import asyncio
from playsound import playsound
import multiprocessing

import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class Alarm(threading.Thread):

    def __init__(self):
        super(Alarm, self).__init__()
        self.keep_running = True
        self.ALARMs = []
        self.DAYS = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES", "SABADO", "DOMINGO"]
        self.alarm_ringing = None

    def add_range_days(self, rangex, timex):
        x_o = rangex.upper().split("-")
        start = self.DAYS.index(x_o[0])
        end = self.DAYS.index(x_o[1])
        for i in range(start, end):
            day_name = self.DAYS[i]
            filtered = [day for day in self.ALARMs if day["DAY"] == day_name and day["TIME"] == timex]
            if not filtered:
                self.ALARMs.append({"DAY": day_name, "TIME": timex, "LASTED": None})

    def add_per_days(self, days, timex):
        x_o = days.upper().split(",")
        for i in x_o:
            day = i.strip()
            index_day = self.DAYS.index(day)
            day_name = self.DAYS[index_day]
            filtered = [day for day in self.ALARMs if day["DAY"] == day_name and day["TIME"] == timex]
            if not filtered:
                self.ALARMs.append({"DAY": day_name, "TIME": timex, "LASTED": None})

    def stop_sound(self):
        if self.alarm_ringing:
            self.alarm_ringing.terminate()

    def start_sound(self):
        self.stop_sound()
        self.alarm_ringing = multiprocessing.Process(target=playsound, args=("data/alarma/sound_alarma_1.mp3",))
        self.alarm_ringing.start()

    def run(self):
        try:
            while self.keep_running:
                now = datetime.datetime.now()
                timex = now.strftime("%H:%M").upper()
                day = now.strftime("%A").upper()
                day_number = now.strftime("%d").upper()
                for x in self.ALARMs:
                    if x["LASTED"]:
                        lasted = x["LASTED"].strftime("%d").upper()
                        if x["DAY"] == day and x["TIME"] == timex and lasted != day_number:
                            x["LASTED"] = now
                            self.start_sound()
                    elif x["DAY"] == day and x["TIME"] == timex:
                        x["LASTED"] = now
                        self.start_sound()
                time.sleep(1)
        except Exception as e:
            print(e)

    def just_die(self):
        self.keep_running = False


a = Alarm()
a.start()
a.add_per_days("LUNES,MARTES", "14:26")
#a.add_range_days("LUNES-MARTES", "14:22")
print("calll")
#time.sleep(10)
