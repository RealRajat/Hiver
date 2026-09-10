from typing import List, Dict, Any, Tuple
try:
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
except ImportError:
    raise ImportError("sklearn is required for metrics calculation. Please install scikit-learn.")

def calculate_intent_metrics(y_true: List[str], y_pred: List[str], labels: List[str]) -> Dict[str, Any]:
    """
    Calculates automated intent metrics:
    - accuracy
    - macro precision, recall, f1
    - per-intent metrics
    - confusion matrix
    """
    
    if not y_true or not y_pred:
        return {}
        
    accuracy = accuracy_score(y_true, y_pred)
    
    # Macro metrics
    macro_p, macro_r, macro_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average='macro', zero_division=0
    )
    
    # Per-intent metrics
    per_intent_p, per_intent_r, per_intent_f1, support = precision_recall_fscore_support(
        y_true, y_pred, labels=labels, average=None, zero_division=0
    )
    
    per_intent = {}
    for i, label in enumerate(labels):
        per_intent[label] = {
            'precision': float(per_intent_p[i]),
            'recall': float(per_intent_r[i]),
            'f1': float(per_intent_f1[i]),
            'support': int(support[i])
        }
        
    # Confusion Matrix
    cm = confusion_matrix(y_true, y_pred, labels=labels)
    cm_dict = {label: {labels[j]: int(cm[i][j]) for j in range(len(labels))} for i, label in enumerate(labels)}
    
    return {
        'accuracy': float(accuracy),
        'macro_precision': float(macro_p),
        'macro_recall': float(macro_r),
        'macro_f1': float(macro_f1),
        'per_intent': per_intent,
        'confusion_matrix': cm_dict
    }

def calculate_agreement_metrics(human_scores: List[float], llm_scores: List[float]) -> Dict[str, float]:
    """
    Calculates agreement between Human and LLM judge scores.
    """
    if not human_scores or not llm_scores or len(human_scores) != len(llm_scores):
        return {}
        
    exact_matches = sum(1 for h, l in zip(human_scores, llm_scores) if h == l)
    within_one = sum(1 for h, l in zip(human_scores, llm_scores) if abs(h - l) <= 1)
    
    mad = sum(abs(h - l) for h, l in zip(human_scores, llm_scores)) / len(human_scores)
    
    return {
        'exact_agreement_pct': exact_matches / len(human_scores),
        'agreement_within_1_pct': within_one / len(human_scores),
        'mean_absolute_difference': mad
    }
