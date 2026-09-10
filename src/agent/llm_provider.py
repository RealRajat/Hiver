from abc import ABC, abstractmethod

class LLMProvider(ABC):
    """
    Abstract interface for LLM calls.
    Allows easy swapping between mock and real providers.
    """
    @abstractmethod
    def generate(self, prompt: str) -> str:
        pass

class MockLLMProvider(LLMProvider):
    """
    A mock provider for testing and environments without API keys.
    Returns predefined deterministic responses to verify structured output parsing.
    """
    def __init__(self, fixed_responses: dict = None):
        self.fixed_responses = fixed_responses or {}
        
    def generate(self, prompt: str) -> str:
        # Simple heuristic to distinguish intent vs response prompts in mock
        if "Classify the following customer support message" in prompt:
            # We mock "Software Bug / Glitch" by default unless overridden
            return self.fixed_responses.get("intent", "Software Bug / Glitch")
        else:
            return self.fixed_responses.get("response", "This is a mocked safe LLM response based on the evidence.")
