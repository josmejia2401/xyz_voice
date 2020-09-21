import abc
import datetime
import random
from category.category import Category


class JokeCategory(Category):

    def __init__(self, xyz_respond = None, xyz_listen = None):
        super().__init__()
        self.xyz_respond = xyz_respond
        self.xyz_listen = xyz_listen
        self.build()
    
    def stop(self):
        pass

    def build(self):
        import locale
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        self.joke = ["hoy es lunes jejejejejeje", "no tengo mas chistes, por favor actualiza mi base de datos."]

    def clean(self, statement):
        statement = statement.replace("cristal", "")
        statement = statement.replace("ey cristal", "")
        statement = statement.replace("hey cristal", "")
        statement = statement.replace("cristal", "")
        return statement.strip()

    def process(self, statement):
        new_statement = self.strip_accents(statement.lower())
        new_statement = self.clean(new_statement)
        respondVal = ""
        if "cuentame un chiste" in new_statement:
            respondVal =  random.choice(self.joke)
        if "echame un chiste" in new_statement:
            respondVal =  random.choice(self.joke)
        if "echate un chiste" in new_statement:
            respondVal =  random.choice(self.joke)
        if "cuenta un chiste" in new_statement:
            respondVal =  random.choice(self.joke)
        if "cuentanos un chiste" in new_statement:
            respondVal =  random.choice(self.joke)
        elif "otro chiste" in new_statement:
            respondVal = random.choice(self.joke)
        return respondVal

    def respond(self, statement):
        return self.process(statement["transcription"])