from gensim.similarities import MatrixSimilarity
from prepropcess import preprocess
from similarity_calc import dictionary, tfidf, bow_corpus


index = MatrixSimilarity(tfidf[bow_corpus]) # index for similarity comparisons

def calculate_similarity(text1, text2):
    bow1 = dictionary.doc2bow(preprocess(text1))
    bow2 = dictionary.doc2bow(preprocess(text2))
    
    tfidf1 = tfidf[bow1]
    tfidf2 = tfidf[bow2]
    
    sims = index[tfidf2]
    
    similarity = sims[bow_corpus.index(bow1)]
    return similarity


text1 = "This is a sample text for article one." #test
text2 = "This is another example text for article two."

similarity = calculate_similarity(text1, text2)
print(f"Similarity: {similarity}")