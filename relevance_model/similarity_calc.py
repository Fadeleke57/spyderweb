from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from .prepropcess import preprocess


corpus = [
    preprocess("This is a sample text for article one."),
    preprocess("This is another example text for article two."),
    preprocess("Yet another example text for article three.")
]


dictionary = Dictionary(corpus) # for the TF-IDF model
bow_corpus = [dictionary.doc2bow(text) for text in corpus]


tfidf = TfidfModel(bow_corpus) # training