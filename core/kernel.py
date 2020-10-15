import re
import random

from core.registry import get_skills
from core.analyzer import SkillAnalyzer


class Kernel:
    
    def __init__(self):
        self.analyzer = SkillAnalyzer()
        self.HISTORY = []

    def respond(self, inputx):
        try:
            sentences = self.analyzer.sentences(inputx)
            response = ""
            for s in sentences:
                self._respond(s)
            return response
        except Exception as e:
            print("respond", e)

    def _respond(self, inputx):
        try:
            if len(inputx) == 0:
                return ""
            ext = self.analyzer.extract(inputx)
            self._processElement(ext)
        except Exception as e:
            print("_respond", e)
            return ""

    def _processElement(self, ext):
        print(ext)
        ext = " ".join(str(e).strip() for e in ext)
        print("ooooooooo",ext)
        response = ""
        skills = get_skills()
        for skill in skills:
            for pat in skill["pattern"]:
                try:
                    pattern = pat
                    pattern = pattern.replace("+", "\+")
                    pattern = pattern.replace("-", "\-")
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
                            func(ext, template, values, self.HISTORY)
                            return
                except Exception as e:
                    print("_processElement", e)
            else:
                continue


# test
if __name__ == "__main__":
    k = Kernel()
