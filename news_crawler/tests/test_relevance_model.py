import pytest
import time
from ..spider_models.relevance_model import RelevanceModel

def test_relevance_model():
    article = """The company's revenue grew by 20% last quarter, driven by strong sales in the electronics division. The CEO announced a new strategic initiative to expand into emerging markets. The board of directors approved a dividend increase to reward shareholders. The marketing team launched a new campaign that significantly boosted brand awareness. The company's supply chain efficiency improved, reducing costs by 15%. The annual general meeting will be held next month to discuss future growth strategies. The research and development department is focusing on innovative technologies to stay ahead of competitors. The company is committed to sustainability and has set ambitious environmental goals. The finance team reported a significant increase in profits due to cost-cutting measures. The customer service department received high satisfaction ratings in the latest survey."""

    
    start_time_nltk = time.time() # measures time taken using NLTK for sentence tokenization
    model_nltk = RelevanceModel(article, use_nltk=True)
    end_time_nltk = time.time()
    time_nltk = end_time_nltk - start_time_nltk

    
    start_time_simple = time.time() # measures time taken using simple string splitting for sentence tokenization
    model_simple = RelevanceModel(article, use_nltk=False)
    end_time_simple = time.time()
    time_simple = end_time_simple - start_time_simple

    
    assert time_simple < time_nltk, "Simple string splitting should be faster than NLTK." # the simple method should be faster than NLTK

    # Define test cases for relevance scores
    test_cases = [
        {
            "text1": "The company's revenue grew by 20% last quarter, driven by strong sales in the electronics division.",
            "text2": "The finance team reported a significant increase in profits due to cost-cutting measures.",
            "expected_similarity": "Moderate to High Similarity"
        },
        {
            "text1": "The CEO announced a new strategic initiative to expand into emerging markets.",
            "text2": "The board of directors approved a dividend increase to reward shareholders.",
            "expected_similarity": "Low to Moderate Similarity"
        },
        {
            "text1": "The marketing team launched a new campaign that significantly boosted brand awareness.",
            "text2": "The customer service department received high satisfaction ratings in the latest survey.",
            "expected_similarity": "Moderate Similarity"
        },
        {
            "text1": "The company's supply chain efficiency improved, reducing costs by 15%.",
            "text2": "The research and development department is focusing on innovative technologies to stay ahead of competitors.",
            "expected_similarity": "Low to Moderate Similarity"
        },
        {
            "text1": "The annual general meeting will be held next month to discuss future growth strategies.",
            "text2": "The company is committed to sustainability and has set ambitious environmental goals.",
            "expected_similarity": "Low Similarity"
        },
        {
            "text1": "The company's revenue grew by 20% last quarter, driven by strong sales in the electronics division.",
            "text2": "Cooking a delicious meal requires fresh ingredients and careful preparation.",
            "expected_similarity": "Very Low Similarity"
        },
        {
            "text1": "The company is committed to sustainability and has set ambitious environmental goals.",
            "text2": "The marketing team launched a new campaign that significantly boosted brand awareness.",
            "expected_similarity": "Low to Moderate Similarity"
        }
    ]

    
    for i, test_case in enumerate(test_cases): # for relevance scores
        text1 = test_case["text1"]
        text2 = test_case["text2"]
        expected_similarity = test_case["expected_similarity"]
        
        score_nltk = model_nltk.get_relevance_score(text1, text2)
        score_simple = model_simple.get_relevance_score(text1, text2)
        
        print(f"Test case {i+1}:")
        print(f"Text 1: {text1}")
        print(f"Text 2: {text2}")
        print(f"Expected similarity: {expected_similarity}")
        print(f"NLTK Relevance score: {score_nltk}")
        print(f"Simple Relevance score: {score_simple}")
        print("----")

if __name__ == "__main__":
    pytest.main()