#!/usr/bin/env python3
from utils.text_number import to_number
from core.skill import AssistantSkill
from utils.mapping import math_symbols_mapping


class MathSkills(AssistantSkill):

    @classmethod
    def do_calculations(cls, ext = None, template = None, values = None, history = []):
        try:
            transcript_with_numbers = cls._replace_words_with_numbers(ext)
            transcript_with_numbers = cls._replace_words_with_math_symbols(transcript_with_numbers)
            math_equation = cls._clear_transcript(transcript_with_numbers)
            result = str(eval(math_equation))
            r = template.format(result)
            cls.response(r)
        except Exception as e:
            r = template.format('Falló al realizar la operación {0} con el mensaje de error {1}'.format(math_equation, e))
            cls.response(r)

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