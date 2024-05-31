import re
from gensim.utils import simple_preprocess
from gensim.parsing.preprocessing import STOPWORDS
from nltk.stem import WordNetLemmatizer, SnowballStemmer

lemmatizer = WordNetLemmatizer() 
stemmer = SnowballStemmer("english") #for future language considerations??

def preprocess(text):
    result = []
    for token in simple_preprocess(text):
        if token not in STOPWORDS and len(token) > 3:
            token = lemmatizer.lemmatize(token)
            token = stemmer.stem(token)
            result.append(token)
    return result