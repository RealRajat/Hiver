import pytest
from src.agent.llm_provider import MockLLMProvider
from src.evaluation.reply_judge import ReplyJudge
from src.evaluation.agreement import calculate_agreement_metrics

def test_reply_judge_valid_json():
    json_response = '{"helpfulness": 4, "correctness": 5, "relevance": 4, "groundedness": 5, "tone": 4, "overall_score": 4, "rationale": "Good"}'
    provider = MockLLMProvider({"response": json_response})
    judge = ReplyJudge(provider)
    
    score = judge.evaluate("msg", "ctx", "reply", "intent")
    assert score["helpfulness"] == 4
    assert score["correctness"] == 5
    assert score["rationale"] == "Good"

def test_reply_judge_invalid_json_fallback():
    provider = MockLLMProvider({"response": "This is not json"})
    judge = ReplyJudge(provider, max_retries=1)
    
    score = judge.evaluate("msg", "ctx", "reply", "intent")
    assert score["overall_score"] == 1
    assert "FAILED_TO_PARSE" in score["rationale"]

def test_reply_judge_missing_fields_fallback():
    json_response = '{"helpfulness": 4}' # Missing other fields
    provider = MockLLMProvider({"response": json_response})
    judge = ReplyJudge(provider, max_retries=1)
    
    score = judge.evaluate("msg", "ctx", "reply", "intent")
    assert score["overall_score"] == 1

def test_reply_judge_out_of_bounds_fallback():
    json_response = '{"helpfulness": 6, "correctness": 5, "relevance": 4, "groundedness": 5, "tone": 4, "overall_score": 4, "rationale": "Good"}'
    provider = MockLLMProvider({"response": json_response})
    judge = ReplyJudge(provider, max_retries=1)
    
    score = judge.evaluate("msg", "ctx", "reply", "intent")
    assert score["overall_score"] == 1

def test_agreement_metrics():
    human = [
        {"helpfulness": 4, "correctness": 5, "relevance": 4, "groundedness": 5, "tone": 4, "overall_score": 4},
        {"helpfulness": 2, "correctness": 2, "relevance": 2, "groundedness": 2, "tone": 2, "overall_score": 2}
    ]
    llm = [
        {"helpfulness": 4, "correctness": 4, "relevance": 4, "groundedness": 5, "tone": 4, "overall_score": 4}, # exact helpfulness, off by 1 correctness
        {"helpfulness": 2, "correctness": 2, "relevance": 2, "groundedness": 2, "tone": 2, "overall_score": 2}
    ]
    
    metrics = calculate_agreement_metrics(human, llm)
    assert metrics["helpfulness"]["exact_agreement"] == 1.0
    assert metrics["correctness"]["exact_agreement"] == 0.5
    assert metrics["correctness"]["within_one_agreement"] == 1.0
