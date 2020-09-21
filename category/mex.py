import abc
import datetime
from category.category import Category


class MeCategory(Category):

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
        if "cual es tu nombre" in new_statement:
            respondVal = "mi nombre es cristal"
        elif "tu nombre" in new_statement:
            respondVal = "mi nombre es cristal"
        if "cual es tu genero" in new_statement:
            respondVal = "mi género es femenino"
        elif "tu genero" in new_statement:
            respondVal = "mi género es femenino"
        return respondVal

    def respond(self, statement):
        return self.process(statement["transcription"])