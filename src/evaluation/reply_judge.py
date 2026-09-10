from typing import TypedDict, Optional
import json
import re
from src.agent.llm_provider import LLMProvider

class ReplyEvaluation(TypedDict):
    helpfulness: int     # 1-5 scale
    correctness: int     # 1-5 scale
    relevance: int       # 1-5 scale
    groundedness: int    # 1-5 scale
    tone: int            # 1-5 scale
    overall_score: int   # 1-5 scale
    rationale: str       # Text explanation of the scoring

class ReplyJudge:
    """
    Evaluates drafted replies using LLM-as-judge with strict JSON output validation.
    """
    
    def __init__(self, provider: LLMProvider, max_retries: int = 3):
        self.provider = provider
        self.max_retries = max_retries
        
    def evaluate(
        self,
        customer_message: str,
        conversation_context: str,
        draft_reply: str,
        predicted_intent: str,
        retrieved_evidence: Optional[str] = None
    ) -> ReplyEvaluation:
        
        prompt = f"""You are an expert customer support QA evaluator. Your task is to score a drafted support reply on a 1-5 scale across 5 dimensions, plus an overall score.

CUSTOMER MESSAGE: "{customer_message}"
PREDICTED INTENT: "{predicted_intent}"
HISTORICAL EVIDENCE: "{retrieved_evidence or 'None'}"
DRAFT REPLY: "{draft_reply}"

INSTRUCTIONS:
1. Score helpfulness, correctness, relevance, groundedness, tone, and overall_score from 1 to 5.
2. Groundedness means the reply stays strictly supported by the historical evidence. Penalize hallucinations heavily.
3. Correctness means it actually addresses the issue without making unsupported factual claims.
4. Provide a brief rationale.
5. You MUST return ONLY valid JSON matching this exact structure:
{{
    "helpfulness": 5,
    "correctness": 5,
    "relevance": 5,
    "groundedness": 5,
    "tone": 5,
    "overall_score": 5,
    "rationale": "..."
}}
"""
        
        for _ in range(self.max_retries):
            response = self.provider.generate(prompt)
            
            # Attempt to extract JSON if wrapped in markdown blocks
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response
                
            try:
                data = json.loads(json_str)
                # Validate schema and types
                required_keys = ["helpfulness", "correctness", "relevance", "groundedness", "tone", "overall_score", "rationale"]
                if not all(k in data for k in required_keys):
                    continue
                    
                # Validate 1-5 ranges for integers
                valid = True
                for k in required_keys[:-1]:  # all except rationale
                    if not isinstance(data[k], int) or data[k] < 1 or data[k] > 5:
                        valid = False
                        break
                        
                if valid and isinstance(data["rationale"], str):
                    return {
                        "helpfulness": data["helpfulness"],
                        "correctness": data["correctness"],
                        "relevance": data["relevance"],
                        "groundedness": data["groundedness"],
                        "tone": data["tone"],
                        "overall_score": data["overall_score"],
                        "rationale": data["rationale"]
                    }
            except json.JSONDecodeError:
                continue
                
        # If all retries fail, return a safe fallback or raise an error.
        # For evaluation robustness, we return a structural zero-score indicator.
        return {
            "helpfulness": 1,
            "correctness": 1,
            "relevance": 1,
            "groundedness": 1,
            "tone": 1,
            "overall_score": 1,
            "rationale": "FAILED_TO_PARSE_LLM_JUDGE"
        }
