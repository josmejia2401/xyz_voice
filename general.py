import abc
import datetime
import wikipedia

class Statement(abc.ABC):

    @abc.abstractmethod
    def clean(self):
        pass

    @abc.abstractmethod
    def respond(self):
        pass

class GeneralStatement(Statement):

    def __init__(self, xyz_respond = None, xyz_listen = None):
        super().__init__()
        self.xyz_respond = xyz_respond
        self.xyz_listen = xyz_listen
        self.build()
    
    def build(self):
        import locale
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    def clean(self, statement):
        statement = statement.replace("cristal", "")
        statement = statement.replace("ey cristal", "")
        statement = statement.replace("hey cristal", "")
        statement = statement.replace("cristal", "")
        return statement

    def regards(self, statement):
        respondVal = ""
        if "apágate ahora" in statement:
            self.xyz_listen.stop()
            respondVal = "Adiós me estoy apagando."
        if "apagate ahora" in statement:
            self.xyz_listen.stop()
            respondVal = "Adiós me estoy apagando."
        if "apagate" in statement:
            self.xyz_listen.stop()
            respondVal = "Adiós me estoy apagando."
        if "apágate" in statement:
            self.xyz_listen.stop()
            respondVal = "Adiós me estoy apagando."
        return respondVal


    def time(self, statement):
        respondVal = ""
        currentDate = datetime.datetime.now()
        # para más: https://www.w3schools.com/python/python_datetime.asp
        if "que hora es" in statement:
            strTime = currentDate.strftime("%H:%M:%S")
            respondVal = f"la hora es {strTime}"
        if "que hora" in statement:
            strTime = currentDate.strftime("%H:%M:%S")
            respondVal = f"la hora es {strTime}"
        if "qué hora es" in statement:
            strTime = currentDate.strftime("%H:%M:%S")
            respondVal = f"la hora es {strTime}"
        if "qué hora" in statement:
            strTime = currentDate.strftime("%H:%M:%S")
            respondVal = f"la hora es {strTime}"
        elif "que día es" in statement:
            strTime = currentDate.strftime("%A %d de %B de %Y")
            respondVal = f"Hoy es {strTime}"
        elif "que día" in statement:
            strTime = currentDate.strftime("%A %d de %B de %Y")
            respondVal = f"Hoy es {strTime}"
        elif "qué día es" in statement:
            strTime = currentDate.strftime("%A %d de %B de %Y")
            respondVal = f"Hoy es {strTime}"
        elif "qué día" in statement:
            strTime = currentDate.strftime("%A %d de %B de %Y")
            respondVal = f"Hoy es {strTime}"
        return respondVal

    def respond(self, statement):
        text = self.clean(statement)
        tmp = self.time(text)
        if tmp:
            self.xyz_respond.run(tmp)
            return 1

        tmp = self.regards(text)
        if tmp:
            self.xyz_respond.run(tmp)
            return 1

        return 0

        
class WikipediaStatement(Statement):

    def __init__(self, xyz_respond = None, xyz_listen = None):
        super().__init__()
        self.xyz_respond = xyz_respond
        self.xyz_listen = xyz_listen
        self.build()
    
    def build(self):
        import locale
        locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
        wikipedia.set_lang("es")

    def clean(self, statement):
        statement = statement.replace("cristal", "")
        statement = statement.replace("ey cristal", "")
        statement = statement.replace("hey cristal", "")
        statement = statement.replace("cristal", "")
        #statement = statement.lower().replace("wikipedia", "")
        return statement

    """
    que es xx en wikipedia
    buscar en wikipedia xx
    buscar en wikipedia que es xx
    """
    def clean_wiki_search(self, statement) -> str:
        statement = statement.replace("en wikipedia", "")
        statement = statement.replace("buscar en wikipedia que es", "")
        statement = statement.replace("buscar en wikipedia", "")
        statement = statement.replace("que es", "")
        statement = statement.replace("wikipedia", "")
        return statement.strip()
    """
    resumen de xx en wikipedia
    buscar resumen de xx en wikipedia
    buscar en wikipedia resumen de xx
    """
    def clean_wiki_summary(self, statement) -> str:
        statement = statement.replace("resumen de", "")
        statement = statement.replace("buscar resumen de", "")
        statement = statement.replace("buscar en wikipedia resumen de", "")
        statement = statement.replace("en wikipedia", "")
        statement = statement.replace("wikipedia", "")
        return statement.strip()

    def wiki(self, statement):
        results = ""
        statement = statement.lower()
        if "que es" in statement:
            statement = self.clean_wiki_search(statement)
            results = wikipedia.search(statement)
        if "qué es" in statement:
            statement = self.clean_wiki_search(statement)
            results = wikipedia.search(statement)
        if "resumen" in statement:
            statement = self.clean_wiki_summary(statement)
            results = wikipedia.summary(statement, sentences=1)
        if isinstance(results, list):
            results = results[0]
        return results

    def respond(self, statement):
        if "wikipedia" in statement.lower():
            text = self.clean(statement)
            tmp = self.wiki(text)
            if tmp:
                self.xyz_respond.run(tmp)
                return 1
            return 0
        else:
            return 0

        
