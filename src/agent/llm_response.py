from typing import List, Dict, Any, Optional
from src.agent.llm_provider import LLMProvider

class LLMResponseGenerator:
    """
    LLM-powered response generator grounded in historical evidence.
    """
    
    def __init__(self, provider: LLMProvider):
        self.provider = provider
        
    def generate(self, customer_message: str, intent: str, evidence: List[Dict[str, Any]]) -> Optional[str]:
        if not evidence:
            return None
            
        # Extract the highest-scoring evidence response
        best_evidence = evidence[0]
        historical_response = best_evidence.get('support_response', '')
        
        if not historical_response:
            return None
            
        prompt = (
            "You are a helpful customer support agent for AppleSupport. "
            "Draft a professional reply to the customer's message based strictly "
            "on the provided historical evidence. Do not invent links, refunds, "
            "policies, or troubleshooting steps that are not explicitly present in the evidence.\n"
            "Do not state that you are an AI.\n\n"
            f"Customer Message: \"{customer_message}\"\n"
            f"Detected Intent: {intent}\n\n"
            f"Historical Evidence to Base Reply On: \"{historical_response}\"\n\n"
            "Draft Reply:"
        )
        
        response = self.provider.generate(prompt).strip()
        return response
