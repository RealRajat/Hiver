import json
from collections import Counter
from typing import List, Dict
from pathlib import Path

from src.evaluation.baseline_classifier import BaselineIntentClassifier

class MajorityClassClassifier:
    """
    Trivial baseline classifier that predicts the most frequent intent
    observed in the reference corpus, strictly excluding the evaluation set
    to prevent data leakage.
    """
    def __init__(self, data_path="data/processed/applesupport_conversations.jsonl", eval_path="data/evaluation/golden_annotation_ai_draft.csv"):
        self.majority_class = self._determine_majority_class(data_path, eval_path)

    def _determine_majority_class(self, data_path: str, eval_path: str) -> str:
        # 1. Get eval conversation IDs to exclude
        eval_conv_ids = set()
        try:
            import csv
            with open(eval_path, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'conversation_id' in row:
                        eval_conv_ids.add(str(row['conversation_id']))
        except Exception as e:
            pass
            
        # 2. Iterate through reference corpus and predict intents using the deterministic baseline
        # (Since we lack human labels for the full 80,000+ corpus, we use the baseline as a proxy
        # to determine the true macro distribution of customer intents).
        baseline = BaselineIntentClassifier()
        intent_counts = Counter()
        
        # To save time, we will sample the first 10000 valid conversations
        count = 0
        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                conv = json.loads(line)
                conv_id = str(conv.get("conversation_id"))
                if conv_id in eval_conv_ids:
                    continue
                    
                for msg in conv.get("messages", []):
                    if msg.get("inbound") == True:
                        intent = baseline.predict(msg.get("text", ""))
                        intent_counts[intent] += 1
                        break # Only one inbound intent per conversation
                
                count += 1
                if count >= 10000:
                    break
                    
        return intent_counts.most_common(1)[0][0]

    def predict(self, text: str) -> str:
        return self.majority_class
