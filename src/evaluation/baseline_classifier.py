import re
from typing import Dict, Any

class BaselineIntentClassifier:
    """
    A deterministic baseline classifier for support intents based on keyword rules.
    This serves as a minimal baseline for evaluation harness testing and will be
    replaced by a model-based classifier in production.
    """
    
    def predict(self, message: str) -> str:
        """
        Predicts one of the 6 intents based on deterministic rules.
        """
        msg = str(message).lower()
        
        # 1. Purchase & Store Operations
        if re.search(r'\b(order|store|buy|purchase|delivery|shipping|bought|ups|fedex|pay|paid)\b', msg):
            return 'Purchase & Store Operations'
            
        # 2. Services & Account
        if re.search(r'\b(password|account|icloud|apple id|subscription|billing|locked out|itunes|login|sign in)\b', msg):
            return 'Services & Account'
            
        # 3. Device Performance / Hardware
        if re.search(r'\b(battery|freeze|freezing|crash|crashing|screen|broke|broken|port|charge|charging|slow|restart)\b', msg):
            return 'Device Performance / Hardware'
            
        # 4. Software Bug / Glitch
        if re.search(r'\b(bug|glitch|update|ios|keyboard|app|software|wifi|bluetooth|stuck|disappeared|issue)\b', msg):
            return 'Software Bug / Glitch'
            
        # 5. How-To / Feature Question
        if re.search(r'\b(how to|how do i|is there a way|where is|can i)\b', msg):
            return 'How-To / Feature Question'
            
        # 6. Fallback
        return 'General Complaint / Venting (Other)'
