import pytest
import time
import os
from ..spider_models.util import build_central_corpus

def test_build_central_corpus():
    search_term = "AI Technology"
    start_time = time.time()
    corpus = build_central_corpus(search_term)
    end_time = time.time()
    
    assert isinstance(corpus, str), "Corpus should be a string"
    assert len(corpus) > 0, "Corpus should not be empty"
    assert "AI" in corpus or "Technology" in corpus, "Corpus should contain relevant content"
    
    elapsed_time = end_time - start_time
    print(f"Time taken to build corpus: {elapsed_time:.2f} seconds")
    
    # Check if the file exists and has the expected content
    output_file_path = f"news_crawler/data/{'_'.join(search_term.lower().split(' '))}_central_corpus.txt"
    assert os.path.exists(output_file_path), f"File {output_file_path} should exist"
    
    with open(output_file_path, 'r', encoding='utf-8') as file:
        file_content = file.read()
        assert file_content == corpus, "File content should match the returned corpus"

if __name__ == "__main__":
    pytest.main()