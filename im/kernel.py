"""
input
{n} = numbers
{t} = Text
{a} = any

proccess
{d} = date
{dt} = datetime
{+} = plus
{-} = substract
{*} = multi
{/} = divide
----------------
{set=name} = set value name
{get=name} = get value name
"""
import re
import random
from datetime import datetime
import json

from utils import sentences


import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class Kernel:
    # module constants
    _globalSessionID = "_global"  # key of the global session (duh)
    _maxHistorySize = 10000  # maximum length of the _inputs and _responses lists
    # maximum number of recursive <srai>/<sr> tags before the response is aborted.
    _maxRecursionDepth = 100
    # special predicate keys
    _dataHistory = "_dataHistory"  # keys to a queue (list) of recent user data
    _inputStack = "_inputStack"   # Should always be empty in between calls to respond()

    def __init__(self):
        self._verboseMode = True
        self._version = "PyAIML 0.8.6"
        #self._respondLock = threading.RLock()
        self._textEncoding = "utf-8"
        # set up the sessions
        self._sessions = {}
        self.categories = {}
        # set up the element processors
        self._elementProcessors = {
            "date":       self._processDate,
            "time":       self._processDateTime,
            "plus":       self._processPlus,
            "subtract":   self._processSubtract,
        }
        with open('standard/plus.json') as json_file:
            data = json.load(json_file)
            self.categories[data["category"]] = data["values"]
        with open('standard/subtract.json') as json_file:
            data = json.load(json_file)
            self.categories[data["category"]] = data["values"]
        with open('standard/date.json') as json_file:
            data = json.load(json_file)
            self.categories[data["category"]] = data["values"]
        with open('standard/time.json') as json_file:
            data = json.load(json_file)
            self.categories[data["category"]] = data["values"]

    """
    re.findall(r".* (.*) \+ (.*)")
    """

    def respond(self, inputx, sessionID=_globalSessionID):
        """Private version of respond(), does the real work."""
        sent = sentences(inputx)
        response = ""
        for s in sent:
            response += self._respond(inputx, sessionID).strip()
        return response

    def _respond(self, inputx, sessionID):
        """Private version of respond(), does the real work."""
        if len(inputx) == 0:
            return ""
        if len(inputx) > self._maxRecursionDepth:
            if self._verboseMode:
                err = "WARNING: maximum recursion depth exceeded (input='%s')" % input.encode(self._textEncoding, 'replace')
                sys.stderr.write(err)
            return ""
        # Procesar input
        return self._processElement(inputx, sessionID).strip()

    def _processElement(self, inputx, sessionID):
        response = ""
        for key in self.categories:
            try:
                value_key = self.categories[key]
                for vk in value_key:
                    pattern = vk["pattern"]
                    pattern = pattern.replace("+", "\+")
                    pattern = pattern.replace("-", "\-")
                    values = re.findall(r''+pattern, inputx)
                    if values:
                        category = vk["category"]
                        templates = vk["templates"]
                        if templates:
                            r = self._templates(category, templates, values, sessionID)
                            if r:
                                response += r
                                break
                        else:
                            continue
                else:
                    continue
            except Exception as e:
                print("_processElement", e)
        return response

    def _templates(self, category, templates, values, sessionID):
        response = ""
        template = random.choice(templates)
        try:
            handlerFunc = self._elementProcessors[category]
            if handlerFunc:
                r = handlerFunc(template, values, sessionID)
                response += r
        except Exception as e:
            print(e)
            pass
        return response

    # {d}
    def _processDate(self, template, values, sessionID):
        currentDate = datetime.now()
        strTime = currentDate.strftime("%A %d de %B de %Y")
        return template.format(strTime)

    # {dt}
    def _processDateTime(self, template, values, sessionID):
        currentDate = datetime.now()
        strTime = currentDate.strftime("%H horas y %M minutos")
        return template.format(strTime)

    # {d}
    def _processPlus(self, template, values, sessionID):
        try:
            sumx = 0
            for v in values:
                for x in range(len(v)):
                    sumx += int(v[x].strip())
            return template.format(sumx)
        except Exception as e:
            return ""

    #_processSubtract
    def _processSubtract(self, template, values, sessionID):
        try:
            sumx = 0
            for v in values:
                for x in range(len(v)):
                    if sumx == 0:
                        sumx = int(v[x].strip())
                    else:
                        sumx -= int(v[x].strip())
            return template.format(sumx)
        except Exception as e:
            return ""

# test
if __name__ == "__main__":
    k = Kernel()
    print(k.respond("1 mas 1"))
    print(k.respond("1 + 1"))
    print(k.respond("-1 + 1"))
    print(k.respond("cuanto es 1 + 1"))
    print(k.respond("1 - 1"))
    print(k.respond("cuanto es 1 - 1"))
    print(k.respond("fecha actual"))
    print(k.respond("hola que dia es hoy"))
    print(k.respond("hora actual"))
    print(k.respond("hola que hora es"))