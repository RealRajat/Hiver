import pytest
from src.agent.llm_provider import MockLLMProvider
from src.agent.llm_intent import LLMIntentClassifier
from src.agent.llm_response import LLMResponseGenerator

def test_mock_provider():
    provider = MockLLMProvider({"intent": "Device Performance / Hardware", "response": "Mock reply"})
    assert provider.generate("Classify the following customer support message") == "Device Performance / Hardware"
    assert provider.generate("Draft a professional reply") == "Mock reply"

def test_llm_intent_classifier_valid():
    provider = MockLLMProvider({"intent": "Device Performance / Hardware"})
    classifier = LLMIntentClassifier(provider)
    intent = classifier.predict("My phone is slow")
    assert intent == "Device Performance / Hardware"

def test_llm_intent_classifier_invalid_fallback():
    # Provide an invalid intent to test fallback behavior
    provider = MockLLMProvider({"intent": "Invalid Intent Type"})
    classifier = LLMIntentClassifier(provider, max_retries=2)
    intent = classifier.predict("Random stuff")
    
    # Should fall back to general complaint
    assert intent == "General Complaint / Venting (Other)"

def test_llm_response_generator():
    provider = MockLLMProvider({"response": "This is a safe mock reply based on evidence."})
    generator = LLMResponseGenerator(provider)
    
    evidence = [{"support_response": "We can help you."}]
    reply = generator.generate("Hello", "Software Bug / Glitch", evidence)
    
    assert reply == "This is a safe mock reply based on evidence."

def test_llm_response_no_evidence():
    provider = MockLLMProvider({"response": "This shouldn't be called"})
    generator = LLMResponseGenerator(provider)
    
    reply = generator.generate("Hello", "Software Bug / Glitch", [])
    assert reply is None
