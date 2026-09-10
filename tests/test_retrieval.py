import pytest
import json
from pathlib import Path
from src.retrieval.resolution_pairs import ResolutionPairExtractor
from src.retrieval.lexical_retriever import LexicalRetriever

@pytest.fixture
def fake_corpus(tmp_path):
    # Create a small valid jsonl corpus
    data = [
        {
            "conversation_id": "1",
            "messages": [
                {"tweet_id": "10", "inbound": True, "text": "My battery is dying"},
                {"tweet_id": "11", "inbound": False, "text": "We can help you test the battery via DM."}
            ]
        },
        {
            "conversation_id": "2",
            "messages": [
                {"tweet_id": "20", "inbound": True, "text": "How do I reset my phone?"},
                {"tweet_id": "21", "inbound": False, "text": "Here is an article on resetting."}
            ]
        },
        {
            "conversation_id": "3",
            "messages": [
                {"tweet_id": "30", "inbound": True, "text": "Battery issue here too"}
            ] # No support response
        }
    ]
    corpus_path = tmp_path / "fake_corpus.jsonl"
    with open(corpus_path, "w") as f:
        for item in data:
            f.write(json.dumps(item) + "\n")
    return corpus_path

def test_resolution_pair_extraction(fake_corpus):
    extractor = ResolutionPairExtractor(corpus_path=str(fake_corpus))
    pairs = extractor.extract_pairs()
    
    # Should only extract convs 1 and 2, because conv 3 lacks a support response
    assert len(pairs) == 2
    assert pairs[0]["conversation_id"] == "1"
    assert pairs[0]["customer_message"] == "My battery is dying"
    assert pairs[0]["support_response"] == "We can help you test the battery via DM."

def test_lexical_retriever_ranking(fake_corpus):
    extractor = ResolutionPairExtractor(corpus_path=str(fake_corpus))
    pairs = extractor.extract_pairs()
    
    retriever = LexicalRetriever(pairs=pairs)
    
    results = retriever.search("battery", top_k=1)
    assert len(results) == 1
    assert results[0]["conversation_id"] == "1"

def test_lexical_retriever_exclusion(fake_corpus):
    extractor = ResolutionPairExtractor(corpus_path=str(fake_corpus))
    pairs = extractor.extract_pairs()
    retriever = LexicalRetriever(pairs=pairs)
    
    # Search for battery, but exclude conversation_id "1" (the actual match)
    results = retriever.search("battery", top_k=1, exclude_conversation_ids=["1"])
    # It should not return conv "1"
    assert all(r["conversation_id"] != "1" for r in results)

def test_empty_query():
    retriever = LexicalRetriever(pairs=[{"conversation_id": "1", "customer_message": "test", "support_response": "resp", "customer_tweet_id": "1"}])
    assert retriever.search("") == []
