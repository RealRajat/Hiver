from typing import List, Dict, Any, Tuple
from src.agent.models import AgentDecision

class EscalationPolicy:
    """
    Explicit escalation component to decide whether an issue can be 
    safely auto-handled or requires a human.
    """
    
    def __init__(self, min_similarity_threshold: float = 0.15):
        self.min_similarity_threshold = min_similarity_threshold

    def evaluate(self, intent: str, evidence: List[Dict[str, Any]]) -> Tuple[AgentDecision, str]:
        """
        Evaluates the intent and retrieved evidence against escalation rules.
        Returns the decision and a reason.
        """
        # Rule 1: Sensitive Accounts/Billing
        if intent in ['Services & Account', 'Purchase & Store Operations']:
            return AgentDecision.HUMAN_ESCALATION, f"{intent} issues frequently require secure account verification or transaction management."
            
        # Rule 2: Ambiguous/Non-Actionable Intent
        if intent == 'General Complaint / Venting (Other)':
            return AgentDecision.HUMAN_ESCALATION, "General complaints and venting require empathetic human handling or are non-actionable."
            
        # Rule 3: Insufficient Evidence
        if not evidence:
            return AgentDecision.HUMAN_ESCALATION, "No historical resolution evidence retrieved."
            
        max_similarity = evidence[0].get('similarity_score', 0.0)
        if max_similarity < self.min_similarity_threshold:
            return AgentDecision.HUMAN_ESCALATION, f"Retrieved evidence similarity ({max_similarity:.3f}) is below the required threshold ({self.min_similarity_threshold})."
            
        # If all rules pass, it's safe to auto-handle
        return AgentDecision.AUTO_HANDLE, ""
