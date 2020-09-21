import abc
import unicodedata

class Category(abc.ABC):

    @abc.abstractmethod
    def build(self):
        pass

    @abc.abstractmethod
    def clean(self):
        pass

    @abc.abstractmethod
    def process(self, statement):
        pass

    @abc.abstractmethod
    def respond(self):
        pass

    def strip_accents(self, text):
        """
        Strip accents from input String.

        :param text: The input string.
        :type text: String.

        :returns: The processed String.
        :rtype: String.
        """
        try:
            text = unicode(text, 'utf-8')
        except (TypeError, NameError): # unicode is a default on python 3 
            pass
        text = unicodedata.normalize('NFD', text)
        text = text.encode('ascii', 'ignore')
        text = text.decode("utf-8")
        return str(text)