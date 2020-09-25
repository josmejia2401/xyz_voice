from spa2num.converter import to_number
from category.skill import AssistantSkill
from utils.mapping import math_symbols_mapping


class MathSkills(AssistantSkill):
    
    @classmethod
    def do_calculations(cls, param1 = None, param2 = None, param3 = None, **kwargs):
        """
        Do basic operations with numbers in digits or in number words
        e.x
            - one plus one = 2
            - 1 + 1 = 2
            - one plus 1 = 2
            - one + one = 2
        # ------------------------------------------------
        # Current Limitations
        # ------------------------------------------------
        * Only basic operators are supported
        * In the text need spaces to understand the input e.g 3+4 it's not working, but 3 + 4 works!
        """
        transcript_with_numbers = cls._replace_words_with_numbers(param1)
        transcript_with_numbers = cls._replace_words_with_math_symbols(transcript_with_numbers)
        math_equation = cls._clear_transcript(transcript_with_numbers)
        try:
            result = str(eval(math_equation))
            cls.response(result)
        except Exception as e:
            cls.console_manager.console_output('Failed to eval the equation --> {0} with error message {1}'.format(math_equation, e))

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
                # If word is not a number words it has 'ValueError'
                # In this case we add the word as it is
                transcript_with_numbers += ' ' + word
        return transcript_with_numbers

    @classmethod
    def _clear_transcript(cls, transcript):
        """
        Keep in transcript only numbers and operators
        """
        cleaned_transcript = ''
        for word in transcript.split():
            if word.isdigit() or word in math_symbols_mapping.values():
                # Add numbers
                cleaned_transcript += word
            else:
                # Add operators
                cleaned_transcript += math_symbols_mapping.get(word, '')
        return cleaned_transcript