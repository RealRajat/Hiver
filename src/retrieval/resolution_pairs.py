import json
from typing import List, Dict, Any
from pathlib import Path

class ResolutionPairExtractor:
    """
    Extracts Customer Issue -> Support Response pairs from conversation JSONL.
    """
    def __init__(self, corpus_path: str = "data/processed/applesupport_conversations.jsonl"):
        self.corpus_path = Path(corpus_path)
        
    def extract_pairs(self) -> List[Dict[str, Any]]:
        """
        Extracts pairs consisting of the first customer message and the immediate 
        subsequent support response from each conversation.
        """
        if not self.corpus_path.exists():
            raise FileNotFoundError(f"Corpus not found at {self.corpus_path}")
            
        pairs = []
        
        with open(self.corpus_path, 'r', encoding='utf-8') as f:
            for line in f:
                conv = json.loads(line)
                messages = conv.get('messages', [])
                
                # Need at least a customer and a support message
                if len(messages) < 2:
                    continue
                    
                # Find the first customer message
                customer_msg = None
                customer_idx = -1
                for i, msg in enumerate(messages):
                    if msg.get('inbound') == True:
                        customer_msg = msg
                        customer_idx = i
                        break
                        
                if not customer_msg:
                    continue
                    
                # Find the immediate subsequent support message
                support_msg = None
                for msg in messages[customer_idx+1:]:
                    if msg.get('inbound') == False:
                        support_msg = msg
                        break
                        
                if customer_msg and support_msg:
                    pairs.append({
                        "conversation_id": str(conv['conversation_id']),
                        "customer_tweet_id": str(customer_msg['tweet_id']),
                        "support_tweet_id": str(support_msg['tweet_id']),
                        "customer_message": customer_msg['text'].replace('\n', ' '),
                        "support_response": support_msg['text'].replace('\n', ' ')
                    })
                    
        return pairs
