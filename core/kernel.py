import re
import random

from core.registry import get_skills
from core.analyzer import SkillAnalyzer

import locale
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

class Kernel:
    def __init__(self):
        self.analyzer = SkillAnalyzer()

    def respond(self, inputx):
        """Private version of respond(), does the real work."""
        sentences = self.analyzer.sentences(inputx)
        response = ""
        for s in sentences:
            response += self._respond(s).strip()
        return response

    def _respond(self, inputx):
        """Private version of respond(), does the real work."""
        if len(inputx) == 0:
            return ""
        ext = self.analyzer.extract(inputx)
        return self._processElement(ext).strip()

    def _processElement(self, ext):
        ext = " ".join(str(e).strip() for e in ext)
        response = ""
        skills = get_skills()
        for skill in skills:
            try:
                pattern = skill["pattern"]
                pattern = pattern.replace("+", "\+")
                pattern = pattern.replace("-", "\-")
                values = re.findall(r''+pattern, ext)
                if values:
                    func = skill["func"]
                    templates = skill["templates"]
                    if templates:
                        template = random.choice(templates)
                        return func(ext, template, values)
            except Exception as e:
                print("_processElement", e)
        return response

# test
if __name__ == "__main__":
    k = Kernel()