import pytest
import pandas as pd
from pathlib import Path
from src.evaluation.golden_loader import GoldenSetLoader
from src.evaluation.baseline_classifier import BaselineIntentClassifier
from src.evaluation.metrics import calculate_intent_metrics, calculate_agreement_metrics
from src.evaluation.reply_judge import ReplyJudge

def test_golden_loader_validates_schema(tmp_path):
    # Create a fake valid CSV
    df = pd.DataFrame({
        'example_id': [f"GOLDEN_{i:03d}" for i in range(1, 201)],
        'conversation_id': [123]*200,
        'tweet_id': [456]*200,
        'customer_message': ["Hello"]*200,
        'optional_context': [""]*200,
        'annotation_status': ["reviewed"]*200,
        'intent': ["Software Bug / Glitch"]*200,
        'ambiguity_flag': [False]*200,
        'annotation_notes': [""]*200,
        'annotation_source': ["human_reviewed"]*200
    })
    csv_file = tmp_path / "fake_golden.csv"
    df.to_csv(csv_file, index=False)
    
    loader = GoldenSetLoader(csv_path=str(csv_file))
    data = loader.load()
    assert len(data) == 200

def test_golden_loader_invalid_schema(tmp_path):
    # Create invalid CSV (199 rows)
    df = pd.DataFrame({'example_id': [f"GOLDEN_{i:03d}" for i in range(1, 200)]})
    csv_file = tmp_path / "fake_invalid.csv"
    df.to_csv(csv_file, index=False)
    
    loader = GoldenSetLoader(csv_path=str(csv_file))
    with pytest.raises(ValueError, match="exactly 200 examples"):
        loader.load()

def test_baseline_classifier_valid_labels():
    classifier = BaselineIntentClassifier()
    assert classifier.predict("battery is dying") == 'Device Performance / Hardware'
    assert classifier.predict("how do i reset?") == 'How-To / Feature Question'
    assert classifier.predict("this is a random complaint") == 'General Complaint / Venting (Other)'
    
def test_metrics_calculation():
    y_true = ['Software Bug / Glitch', 'Device Performance / Hardware']
    y_pred = ['Software Bug / Glitch', 'General Complaint / Venting (Other)']
    labels = list(GoldenSetLoader.VALID_INTENTS)
    
    metrics = calculate_intent_metrics(y_true, y_pred, labels)
    assert metrics['accuracy'] == 0.5
    assert 'Software Bug / Glitch' in metrics['confusion_matrix']

def test_agreement_metrics():
    human = [5.0, 4.0, 3.0]
    llm = [5.0, 3.0, 1.0]
    metrics = calculate_agreement_metrics(human, llm)
    assert metrics['exact_agreement_pct'] == 1/3
    assert metrics['agreement_within_1_pct'] == 2/3
    assert metrics['mean_absolute_difference'] == (0 + 1 + 2) / 3

def test_reply_judge_interface():
    from src.agent.llm_provider import MockLLMProvider
    provider = MockLLMProvider({"response": '{"helpfulness": 5, "correctness": 5, "relevance": 5, "groundedness": 5, "tone": 5, "overall_score": 5, "rationale": "Mock"}'})
    judge = ReplyJudge(provider)
    result = judge.evaluate(
        customer_message="msg", 
        conversation_context="ctx", 
        draft_reply="reply", 
        predicted_intent="intent"
    )
    assert result["overall_score"] == 5
