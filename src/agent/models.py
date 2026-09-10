from enum import Enum
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict

class AgentDecision(str, Enum):
    AUTO_HANDLE = "AUTO_HANDLE"
    HUMAN_ESCALATION = "HUMAN_ESCALATION"

@dataclass
class AgentResult:
    customer_message: str
    intent: str
    evidence: List[Dict[str, Any]]
    decision: AgentDecision
    draft_reply: Optional[str] = None
    escalation_reason: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
