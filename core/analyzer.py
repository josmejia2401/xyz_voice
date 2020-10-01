import nltk
nltk.download('stopwords')
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.data import load
from nltk.stem import SnowballStemmer
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

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
        # remove accents
        text = self.strip_accents(text)
        # remove links from tweets
        text = re.sub(r"http\S+", "https", text)
        # remove punctuation
        #text = ''.join([c for c in text if c not in self.non_words])
        #print("4", text)
        # remove repeated characters
        text = re.sub(r'(.)\1+', r'\1\1', text)
        # tokenize
        tokens = word_tokenize(text)
        # clean tokens
        #6 ['crear', 'alarma', 'el', 'lunes', 'a', 'las', '8:15']
        #7 ['crear', 'alarma', 'lunes', '8:15']
        # tokens = [w for w in tokens if not w in self.spanish_stopwords]
        #WP	WH-pronoun
        #NNP	Proper noun, singular
        #NN	noun, singular
        #.	Punctuation marks
        #tagged = pos_tag(clean_tokens)
        #tokens = self.get_continuous_chunks(text)
        # stem
        """try:
            stems = self.stem_tokens(tokens, self.stemmer)
        except Exception as e:
            print(e)
            print(text)
            stems = ['']
        return stems"""
        return tokens
    def get_continuous_chunks(self, text):
        chunked = ne_chunk(pos_tag(word_tokenize(text)))
        # clean tokens
        chunked = [w for w in chunked if not w in spanish_stopwords]    
        prev = None
        continuous_chunk = []
        current_chunk = []

        for i in chunked:
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                    current_chunk = []
            else:
                continue

        if continuous_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)

        return continuous_chunk

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

    def sentences(self, s):
        """Split the string s into a list of sentences."""
        try: 
            s + ""
        except: 
            raise TypeError("s must be a string")
        pos = 0
        sentenceList = []
        l = len(s)
        while pos < l:
            try: p = s.index('.', pos)
            except: p = l+1
            try: q = s.index('?', pos)
            except: q = l+1
            try: e = s.index('!', pos)
            except: e = l+1
            end = min(p,q,e)
            sentenceList.append( s[pos:end].strip() )
            pos = end+1
        if len(sentenceList) == 0: sentenceList.append(s)
        return sentenceList