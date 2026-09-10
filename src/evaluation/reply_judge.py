from typing import TypedDict, Optional

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
    Interface for evaluating drafted replies using LLM-as-judge.
    This serves as the foundational schema preparation. 
    Actual LLM integration will be implemented in future phases.
    """
    
    def evaluate(
        self,
        customer_message: str,
        conversation_context: str,
        draft_reply: str,
        retrieved_evidence: Optional[str] = None
    ) -> ReplyEvaluation:
        """
        Evaluates a draft reply against the customer message and context.
        Returns a structured ReplyEvaluation.
        """
        raise NotImplementedError("LLM integration not yet implemented. This is an interface stub.")
