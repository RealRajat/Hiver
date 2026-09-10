import pytest
from src.agent.models import AgentDecision, AgentResult
from src.agent.escalation import EscalationPolicy
from src.agent.response import ResponseGenerator
from src.agent.agent import SupportAgent

def test_escalation_sensitive_intent():
    policy = EscalationPolicy()
    decision, reason = policy.evaluate("Services & Account", [{"similarity_score": 0.9}])
    assert decision == AgentDecision.HUMAN_ESCALATION
    assert "secure account verification" in reason

def test_escalation_no_evidence():
    policy = EscalationPolicy()
    decision, reason = policy.evaluate("Software Bug / Glitch", [])
    assert decision == AgentDecision.HUMAN_ESCALATION
    assert "No historical resolution evidence" in reason

def test_escalation_low_similarity():
    policy = EscalationPolicy(min_similarity_threshold=0.5)
    decision, reason = policy.evaluate("Software Bug / Glitch", [{"similarity_score": 0.4}])
    assert decision == AgentDecision.HUMAN_ESCALATION
    assert "below the required threshold" in reason

def test_auto_handle_safe():
    policy = EscalationPolicy(min_similarity_threshold=0.1)
    decision, reason = policy.evaluate("Software Bug / Glitch", [{"similarity_score": 0.2}])
    assert decision == AgentDecision.AUTO_HANDLE
    assert reason == ""

def test_deterministic_response_generation():
    generator = ResponseGenerator()
    evidence = [{"support_response": "Please restart your device."}]
    reply = generator.generate("It crashed", "Software Bug / Glitch", evidence)
    assert "Please restart your device." in reply
    assert "Apple Support typically advises" in reply

def test_agent_orchestration(monkeypatch):
    agent = SupportAgent()
    
    # Mock classifier and retriever to isolate agent testing
    class MockClassifier:
        def predict(self, msg): return "Software Bug / Glitch"
    
    class MockRetriever:
        def search(self, query, top_k, exclude_conversation_ids):
            # Record that the exclusion parameter was properly passed
            self.last_exclude = exclude_conversation_ids
            return [{"customer_message": "bug", "support_response": "fixed", "similarity_score": 0.9}]
            
    agent.classifier = MockClassifier()
    agent.retriever = MockRetriever()
    
    result = agent.run("My app crashed", conversation_id="123")
    
    assert result.decision == AgentDecision.AUTO_HANDLE
    assert result.intent == "Software Bug / Glitch"
    assert "fixed" in result.draft_reply
    # Verify leakage prevention
    assert "123" in agent.retriever.last_exclude

def test_agent_orchestration_escalation():
    agent = SupportAgent()
    
    class MockClassifier:
        def predict(self, msg): return "Services & Account"
        
    class MockRetriever:
        def search(self, query, top_k, exclude_conversation_ids):
            return [{"customer_message": "login", "support_response": "reset", "similarity_score": 0.9}]
            
    agent.classifier = MockClassifier()
    agent.retriever = MockRetriever()
    
    result = agent.run("I am locked out")
    
    assert result.decision == AgentDecision.HUMAN_ESCALATION
    assert result.draft_reply is None
    assert result.escalation_reason is not None
