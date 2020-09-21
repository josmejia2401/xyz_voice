import abc
import datetime
from category.category import Category

class TimeCategory(Category):

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
        currentDate = datetime.datetime.now()
        # para más: https://www.w3schools.com/python/python_datetime.asp
        if "que hora es" in new_statement:
            strTime = currentDate.strftime("%H:%M:%S")
            respondVal = f"la hora es {strTime}"
        if "que hora" in new_statement:
            strTime = currentDate.strftime("%H:%M:%S")
            respondVal = f"la hora es {strTime}"
        if "qué hora es" in new_statement:
            strTime = currentDate.strftime("%H:%M:%S")
            respondVal = f"la hora es {strTime}"
        if "qué hora" in new_statement:
            strTime = currentDate.strftime("%H:%M:%S")
            respondVal = f"la hora es {strTime}"
        elif "que día es" in new_statement:
            strTime = currentDate.strftime("%A %d de %B de %Y")
            respondVal = f"Hoy es {strTime}"
        elif "que día" in new_statement:
            strTime = currentDate.strftime("%A %d de %B de %Y")
            respondVal = f"Hoy es {strTime}"
        elif "qué día es" in new_statement:
            strTime = currentDate.strftime("%A %d de %B de %Y")
            respondVal = f"Hoy es {strTime}"
        elif "qué día" in new_statement:
            strTime = currentDate.strftime("%A %d de %B de %Y")
            respondVal = f"Hoy es {strTime}"
        return respondVal

    def respond(self, statement):
        return self.process(statement["transcription"])