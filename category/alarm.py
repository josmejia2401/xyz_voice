#!/usr/bin/env python3
import abc
import datetime
from category.category import Category
from apps.alarm import Alarm

class AlarmCategory(Category):

    def __init__(self, xyz_respond = None, xyz_listen = None):
        super().__init__()
        self.xyz_respond = xyz_respond
        self.xyz_listen = xyz_listen
        self.build()
    
    def stop(self):
        if self.alarm_app:
            self.alarm_app.stop_sound()
        self.alarm_app.just_die()

    def build(self):
        import locale
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.alarm_app = None

    def clean(self, statement):
        statement = statement.replace("cristal", "")
        statement = statement.replace("ey cristal", "")
        statement = statement.replace("hey cristal", "")
        statement = statement.replace("cristal", "")
        return statement.strip()

    def get_alarm(self):
        if self.alarm_app:
            return self.alarm_app
        else:
            self.alarm_app = Alarm()
            self.alarm_app.start()
            return self.alarm_app

    def process(self, statement):
        new_statement = self.strip_accents(statement.lower())
        new_statement = self.clean(new_statement)
        new_statement = new_statement.replace("poner", "")
        new_statement = new_statement.replace("colocar", "")
        new_statement = new_statement.replace("establecer", "")
        new_statement = new_statement.replace("Poner", "")
        new_statement = new_statement.replace("Colocar", "")
        new_statement = new_statement.replace("Establecer", "")

        respondVal = ""
        if "alarma de lunes a viernes a las" in new_statement:
            new_statement = new_statement.replace("alarma de lunes a viernes a las", "")
            xx = ""
            if "y" in new_statement:
                new_statement = new_statement.split("y")
                new_statement = new_statement[0].strip() + ":" + new_statement[1].strip()
            if ":" in new_statement:
                new_statement = new_statement.strip()
            self.get_alarm().add_range_days("LUNES-VIERNES", new_statement)
            respondVal = "alarma establecida de lunes a viernes a las " + new_statement
            
        elif "alarma los dias" in new_statement:
            new_statement = new_statement.replace("alarma los dias", "")
            xx = ""
            if "y" in new_statement:
                new_statement = new_statement.split("y")
                new_statement = new_statement[0].strip() + ":" + new_statement[1].strip()
            if ":" in new_statement:
                new_statement = new_statement.strip()
            respondVal = "alarma establecida los dias a las " + new_statement
        return respondVal

    def respond(self, statement):
        return self.process(statement["transcription"])