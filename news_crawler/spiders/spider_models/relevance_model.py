from gensim.similarities import MatrixSimilarity
from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from .prepropcess import preprocess

class Relevance_Model:

    def find_relevance(self):
        similarity = self.calculate_similarity()
        return similarity #format return type later
    
    def calculate_similarity(self, text1, text2):
        corpus = [preprocess(text1), preprocess(text2)]
        dictionary = Dictionary(corpus)
        bow_corpus = [dictionary.doc2bow(text) for text in corpus]

        tfidf = TfidfModel(bow_corpus) #create frequency model
        index = MatrixSimilarity(tfidf[bow_corpus]) #training model
        bow1 = dictionary.doc2bow(preprocess(text1))
        bow2 = dictionary.doc2bow(preprocess(text2))
        tfidf1 = tfidf[bow1]
        tfidf2 = tfidf[bow2]
        
        sims = index[tfidf2]
        
        similarity = sims[self.bow_corpus.index(bow1)]
        return similarity