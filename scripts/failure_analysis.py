import json
from collections import defaultdict, Counter
from pathlib import Path

def main():
    reports_dir = Path("reports")
    agent_results_path = reports_dir / "agent_evaluation_baseline.json"
    
    if not agent_results_path.exists():
        print("Baseline results not found.")
        return
        
    with open(agent_results_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    examples = data.get("examples", [])
    
    print("\n" + "="*50)
    print("PHASE 7 - FAILURE ANALYSIS PROGRAMMATIC EXTRACT")
    print("="*50)
    
    # 1. Intent Confusion
    print("\n--- INTENT CONFUSIONS ---")
    confusions = Counter()
    for ex in examples:
        true_intent = ex.get("gold_intent")
        pred_intent = ex.get("predicted_intent")
        if true_intent != pred_intent:
            confusions[(true_intent, pred_intent)] += 1
            
    for (t, p), count in confusions.most_common(5):
        print(f"True: '{t}' | Pred: '{p}' -> {count} times")
        
    # 2. Retrieval Failures (Low proxy hit rate or similarity)
    print("\n--- RETRIEVAL FAILURES ---")
    proxy_misses = [ex for ex in examples if not ex.get("proxy_hit")]
    print(f"Total Retrieval Proxy Misses: {len(proxy_misses)}")
    if proxy_misses:
        sample = proxy_misses[0]
        print(f"Sample Proxy Miss Example ID: {sample['example_id']}")
        print(f"Message: {sample['customer_message']}")
        
    # 3. Escalation Analysis
    print("\n--- ESCALATION ANALYSIS ---")
    escalated = [ex for ex in examples if ex.get("decision") == "HUMAN_ESCALATION"]
    auto_handled = [ex for ex in examples if ex.get("decision") == "AUTO_HANDLE"]
    
    print(f"Total Escalated: {len(escalated)} ({len(escalated)/len(examples)*100:.1f}%)")
    print(f"Total Auto-Handled: {len(auto_handled)} ({len(auto_handled)/len(examples)*100:.1f}%)")
    
    escalated_by_intent = Counter(ex.get("predicted_intent") for ex in escalated)
    print("\nEscalation by Predicted Intent:")
    for intent, count in escalated_by_intent.most_common():
        print(f"- {intent}: {count}")

if __name__ == "__main__":
    main()
