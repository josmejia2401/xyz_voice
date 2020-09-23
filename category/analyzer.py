import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk import word_tokenize
from nltk.data import load
from nltk.stem import SnowballStemmer
from string import punctuation
import re
from utils.mapping import math_symbols_mapping
import unicodedata

class SkillAnalyzer:

    def __init__(self):
        #stopword list to use
        self.spanish_stopwords = stopwords.words('spanish')
        #spanish stemmer
        self.stemmer = SnowballStemmer('spanish')
        #punctuation to remove
        self.non_words = list(punctuation)
        #we add spanish punctuation
        self.non_words.extend(['¿', '¡'])
        #self.non_words.extend(map(str,range(10)))
        self.stemmer = SnowballStemmer('spanish')

    def extract(self, user_transcript):
        user_transcript_with_replaced_math_symbols = self._replace_math_symbols_with_words(user_transcript)
        return self.tokenize(user_transcript_with_replaced_math_symbols)

    def _replace_math_symbols_with_words(self, transcript):
        replaced_transcript = ''
        for word in transcript.split():
            if word in math_symbols_mapping.values():
                for key, value in math_symbols_mapping.items():
                    if value == word:
                        replaced_transcript += ' ' + key
            else:
                replaced_transcript += ' ' + word
        return replaced_transcript

    
    def stem_tokens(self, tokens, stemmer):
        stemmed = []
        for item in tokens:
            stemmed.append(stemmer.stem(item))
        return stemmed

    def tokenize(self, text):
        text = self.strip_accents(text)
        # remove links from tweets
        text = re.sub(r"http\S+", "https", text)
        # remove punctuation
        text = ''.join([c for c in text if c not in self.non_words])
        # remove repeated characters
        text = re.sub(r'(.)\1+', r'\1\1', text)
        # tokenize
        tokens = word_tokenize(text)
        # stem
        """try:
            stems = self.stem_tokens(tokens, self.stemmer)
        except Exception as e:
            print(e)
            print(text)
            stems = ['']
        return stems"""
        return tokens

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