import pandas as pd
import numpy as np
from typing import Dict, Any, List

def calculate_agreement_metrics(human_scores: List[Dict[str, Any]], llm_scores: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates agreement metrics between human judges and the LLM-as-judge.
    Expects lists of dictionaries containing keys: 
    helpfulness, correctness, relevance, groundedness, tone, overall_score
    """
    
    if not human_scores or not llm_scores or len(human_scores) != len(llm_scores):
        return {}
        
    dimensions = ["helpfulness", "correctness", "relevance", "groundedness", "tone", "overall_score"]
    
    metrics = {}
    
    for dim in dimensions:
        h_vals = np.array([x[dim] for x in human_scores])
        l_vals = np.array([x[dim] for x in llm_scores])
        
        exact_match = np.mean(h_vals == l_vals)
        within_one = np.mean(np.abs(h_vals - l_vals) <= 1)
        mean_abs_diff = np.mean(np.abs(h_vals - l_vals))
        
        metrics[dim] = {
            "exact_agreement": float(exact_match),
            "within_one_agreement": float(within_one),
            "mean_abs_diff": float(mean_abs_diff)
        }
        
    # Calculate overall aggregate metrics
    all_exact = [metrics[d]["exact_agreement"] for d in dimensions]
    all_within_one = [metrics[d]["within_one_agreement"] for d in dimensions]
    
    metrics["aggregate"] = {
        "avg_exact_agreement": float(np.mean(all_exact)),
        "avg_within_one_agreement": float(np.mean(all_within_one))
    }
    
    return metrics
