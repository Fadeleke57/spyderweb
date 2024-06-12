import pytest
import time
import os
from ..spider_models.util import build_central_corpus

def test_build_central_corpus():
    for search_term in search_terms:
        start_time = time.time()
        corpus = build_central_corpus(search_term, "data")
        end_time = time.time()
        
        assert isinstance(corpus, str), "Corpus should be a string"
        assert len(corpus) > 0, "Corpus should not be empty"
        terms = search_term.split(" ")
        for term in terms:
            assert term in corpus, f"Corpus should contain '{term}'"
        
        elapsed_time = end_time - start_time
        print(f"Time taken to build this corpus: {elapsed_time:.2f} seconds\n")

        output_file_path = f"data/{'_'.join(search_term.lower().split(' '))}_central_corpus.txt" #check if the file exists and has the expected content
        assert os.path.exists(output_file_path), f"File {output_file_path} should exist"
        
        with open(output_file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()
            assert file_content == corpus, "File content should match the returned corpus"

search_terms = ["Saudi Arabia", "Israel", "Taylor Swift", "Elon Musk", "Apple", "Nvidia", "Tesla"]

if __name__ == "__main__":
    pytest.main()