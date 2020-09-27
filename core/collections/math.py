from spa2num.converter import to_number
from core.skill import AssistantSkill
from utils.mapping import math_symbols_mapping


class MathSkills(AssistantSkill):
    """
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
    """
    @classmethod
    def do_calculations(cls, ext = None, template = None, values = None):
        print(param1)
        transcript_with_numbers = cls._replace_words_with_numbers(param1)
        transcript_with_numbers = cls._replace_words_with_math_symbols(transcript_with_numbers)
        math_equation = cls._clear_transcript(transcript_with_numbers)
        try:
            result = str(eval(math_equation))
            return template.format(result)
        except Exception as e:
            return template.format('Falló al realizar la operación {0} con el mensaje de error {1}'.format(math_equation, e))

    @classmethod
    def _replace_words_with_math_symbols(cls, transcript):
        replaced_transcript = ''
        for word in transcript.split():
            if word in math_symbols_mapping.values():
                for key, value in math_symbols_mapping.items():
                    if key == word:
                        replaced_transcript += ' ' + value
            else:
                replaced_transcript += ' ' + word
        return replaced_transcript

    @classmethod
    def _replace_words_with_numbers(cls, transcript):
        transcript_with_numbers = ''
        for word in transcript.split():
            try:
                number = to_number(word)
                transcript_with_numbers += ' ' + str(number)
            except ValueError as e:
                transcript_with_numbers += ' ' + word
        return transcript_with_numbers

    @classmethod
    def _clear_transcript(cls, transcript):
        cleaned_transcript = ''
        for word in transcript.split():
            if word.isdigit() or word in math_symbols_mapping.values():
                cleaned_transcript += word
            else:
                cleaned_transcript += math_symbols_mapping.get(word, '')
        return cleaned_transcript