import re
import random

from core.registry import get_skills
from core.analyzer import SkillAnalyzer

import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class Kernel:
    def __init__(self):
        self.analyzer = SkillAnalyzer()
        self.HISTORY = []

    def respond(self, inputx):
        """Private version of respond(), does the real work."""
        try:
            sentences = self.analyzer.sentences(inputx)
            response = ""
            for s in sentences:
                response += self._respond(s).strip()
            
            print("**************", response)
            return response
        except Exception as e:
            print("respond", e)

    def _respond(self, inputx):
        """Private version of respond(), does the real work."""
        try:
            if len(inputx) == 0:
                return ""
            ext = self.analyzer.extract(inputx)
            return self._processElement(ext).strip()
        except Exception as e:
            print("_respond", e)
            return ""

    def _processElement(self, ext):
        ext = " ".join(str(e).strip() for e in ext)
        response = ""
        skills = get_skills()
        for skill in skills:
            for pat in skill["pattern"]:
                try:
                    
                    pattern = pat
                    pattern = pattern.replace("+", "\+")
                    pattern = pattern.replace("-", "\-")
                    #pattern = pattern.replace("d*", "\d*")
                    #ext = ext.replace(":", " y ")
                    values = re.findall(r''+pattern, ext)
                    
                    
                    if values:
                        func = skill["func"]
                        templates = skill["templates"]
                        if templates:
                            template = random.choice(templates)
                            print(ext)
                            print(pat)
                            print(values)
                            print("template", template)
                            return func(ext, template, values, self.HISTORY)
                except Exception as e:
                    print("_processElement", e)
            else:
                continue
        return response

# test
if __name__ == "__main__":
    k = Kernel()