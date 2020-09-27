from category.skill import AssistantSkill
import re

class ConversationSkills(AssistantSkill):
    BRAIN = []
    EXPRESSIONS = [
        "C_0": {
            "exp" : "(cual|como)(.+?)(nombre|llamas)",
            "responses" : ["Mi nombre es Cristal y el tuyo cuál es?", "Cristal, y cuál es tú nombre?"]
        },
        "C_1": {
            "exp" : ".*llamo(.*)y tu.*",
            "responses" : ["Hola {}", "{}"]
        },
        "C_1": {
            "exp" : ".*llamo (.*)",
            "responses" : ["Hola {}", "{}"]
        }
    ]

    @classmethod
    def conversation(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        Stop assistant speech.
        """
        #stop_speaking = True
        m = re.search('cual(.+?)nombre', text)
        if m:
            found = m.group(1)
            print("aaaaa", found)

        pass