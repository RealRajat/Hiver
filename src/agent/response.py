from typing import List, Dict, Any, Optional

class ResponseGenerator:
    """
    Deterministic response generator that safely grounds replies 
    in historical evidence. This serves as a precursor to LLM generation.
    """
    
    def generate(self, customer_message: str, intent: str, evidence: List[Dict[str, Any]]) -> Optional[str]:
        """
        Generates a deterministic draft reply based purely on the highest-scoring evidence.
        """
        if not evidence:
            return None
            
        # We rely on the top evidence pair because they are already sorted by similarity
        best_evidence = evidence[0]
        historical_response = best_evidence.get('support_response', '')
        
        if not historical_response:
            return None
            
        # Formulate a safe wrapper around the retrieved response to ensure
        # the user understands its origin and avoids hallucinating direct capabilities.
        draft = (
            f"Based on historical cases with similar {intent} issues, "
            f"Apple Support typically advises:\n\n"
            f"\"{historical_response}\""
        )
        return draft
