from typing import Optional, List
from src.agent.models import AgentResult, AgentDecision
from src.agent.escalation import EscalationPolicy
from src.agent.response import ResponseGenerator
from src.evaluation.baseline_classifier import BaselineIntentClassifier
from src.retrieval.lexical_retriever import LexicalRetriever

class SupportAgent:
    """
    Orchestrates the support pipeline:
    Intent Classification -> Retrieval -> Escalation -> Response Generation
    """
    
    def __init__(self, 
                 classifier: Optional[BaselineIntentClassifier] = None, 
                 retriever: Optional[LexicalRetriever] = None,
                 escalation_policy: Optional[EscalationPolicy] = None,
                 response_generator: Optional[ResponseGenerator] = None):
                 
        self.classifier = classifier or BaselineIntentClassifier()
        self.retriever = retriever or LexicalRetriever()
        self.escalation_policy = escalation_policy or EscalationPolicy()
        self.response_generator = response_generator or ResponseGenerator()

    def run(self, 
            customer_message: str, 
            conversation_id: Optional[str] = None,
            top_k: int = 5) -> AgentResult:
        """
        Executes the end-to-end support pipeline.
        """
        
        # 1. Intent Classification
        intent = self.classifier.predict(customer_message)
        
        # 2. Historical Evidence Retrieval
        exclude_ids = [conversation_id] if conversation_id else []
        evidence = self.retriever.search(
            query=customer_message, 
            top_k=top_k, 
            exclude_conversation_ids=exclude_ids
        )
        
        # 3. Escalation Policy Evaluation
        decision, reason = self.escalation_policy.evaluate(intent, evidence)
        
        # 4. Response Generation
        draft_reply = None
        if decision == AgentDecision.AUTO_HANDLE:
            draft_reply = self.response_generator.generate(customer_message, intent, evidence)
            
        return AgentResult(
            customer_message=customer_message,
            intent=intent,
            evidence=evidence,
            decision=decision,
            draft_reply=draft_reply,
            escalation_reason=reason if reason else None
        )
