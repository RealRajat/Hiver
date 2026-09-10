from typing import List, Dict, Any, Optional
from abc import ABC, abstractmethod

class BaseRetriever(ABC):
    """
    Interface for retrieval components.
    """
    
    @abstractmethod
    def search(self, query: str, top_k: int = 5, exclude_conversation_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        """
        Searches the corpus for the query.
        
        Args:
            query: The customer message to find evidence for.
            top_k: Number of results to return.
            exclude_conversation_ids: List of conversation IDs to ignore (to prevent data leakage).
            
        Returns:
            List of structured dictionary results:
            {
                "conversation_id": "...",
                "customer_message": "...",
                "support_response": "...",
                "similarity_score": float,
                "retrieval_method": "..."
            }
        """
        pass
