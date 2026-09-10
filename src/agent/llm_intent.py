from typing import Optional
from src.agent.llm_provider import LLMProvider
from src.evaluation.golden_loader import GoldenSetLoader

class LLMIntentClassifier:
    """
    LLM-powered intent classifier with structured output validation and bounded retries.
    Falls back to a default category if the LLM repeatedly hallucinates invalid intents.
    """
    
    def __init__(self, provider: LLMProvider, max_retries: int = 3):
        self.provider = provider
        self.max_retries = max_retries
        self.valid_intents = GoldenSetLoader.VALID_INTENTS
        
    def predict(self, message: str) -> str:
        prompt = (
            "Classify the following customer support message into EXACTLY ONE of "
            "the following categories. Return ONLY the category name, nothing else.\n\n"
            "Categories:\n"
            "- Software Bug / Glitch\n"
            "- Device Performance / Hardware\n"
            "- Purchase & Store Operations\n"
            "- Services & Account\n"
            "- How-To / Feature Question\n"
            "- General Complaint / Venting (Other)\n\n"
            f"Message: \"{message}\"\n\n"
            "Category:"
        )
        
        for _ in range(self.max_retries):
            response = self.provider.generate(prompt).strip()
            
            # Clean up potential LLM verbosity (e.g. quotes or markdown)
            clean_response = response.strip('"\'*` \n')
            
            # Exact match validation
            if clean_response in self.valid_intents:
                return clean_response
                
        # Graceful fallback after bounded retries fail
        return 'General Complaint / Venting (Other)'
