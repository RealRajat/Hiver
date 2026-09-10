import json
from pathlib import Path
from src.evaluation.golden_loader import GoldenSetLoader
from src.agent.agent import SupportAgent
from src.evaluation.metrics import calculate_intent_metrics
from src.agent.models import AgentDecision

def main():
    print("Loading Golden Set...")
    loader = GoldenSetLoader()
    dataset = loader.load()
    
    print("Initializing Agent Pipeline (Intent + Retrieval + Escalation + Generation)...")
    agent = SupportAgent()
    
    total_queries = len(dataset)
    y_true_intent = []
    y_pred_intent = []
    
    retrieval_hits = 0
    proxy_intent_hits = 0
    
    auto_handle_count = 0
    escalation_count = 0
    
    results_output = []
    
    # Track stats
    for i, example in enumerate(dataset):
        if i % 20 == 0:
            print(f"Processing {i}/{total_queries}...")
            
        gold_intent = example['intent']
        conv_id = str(example['conversation_id'])
        msg = example['customer_message']
        
        result = agent.run(customer_message=msg, conversation_id=conv_id)
        
        # Intent metrics
        y_true_intent.append(gold_intent)
        y_pred_intent.append(result.intent)
        
        # Retrieval metrics
        if result.evidence:
            retrieval_hits += 1
            # Check proxy match for the top result
            top_ev = result.evidence[0]
            if agent.classifier.predict(top_ev['customer_message']) == gold_intent:
                proxy_intent_hits += 1
                
        # Agent metrics
        if result.decision == AgentDecision.AUTO_HANDLE:
            auto_handle_count += 1
        else:
            escalation_count += 1
            
        # Compile result
        results_output.append({
            "example_id": example['example_id'],
            "customer_message": msg,
            "gold_intent": gold_intent,
            "predicted_intent": result.intent,
            "decision": result.decision.value,
            "escalation_reason": result.escalation_reason,
            "draft_reply": result.draft_reply,
            "top_evidence_sim": result.evidence[0]['similarity_score'] if result.evidence else 0.0
        })
        
    print("Calculating metrics...")
    labels = list(GoldenSetLoader.VALID_INTENTS)
    intent_metrics = calculate_intent_metrics(y_true_intent, y_pred_intent, labels)
    
    retrieval_coverage = retrieval_hits / total_queries
    proxy_hit_rate = proxy_intent_hits / total_queries
    auto_handle_rate = auto_handle_count / total_queries
    escalation_rate = escalation_count / total_queries
    
    # Formatting Markdown Report
    md_lines = [
        "# Agent Pipeline Evaluation Report\n",
        f"**Evaluation Size**: {total_queries} examples\n",
        "## Intent Metrics",
        f"- **Accuracy**: {intent_metrics.get('accuracy', 0):.4f}",
        f"- **Macro F1**: {intent_metrics.get('macro_f1', 0):.4f}\n",
        "## Retrieval Metrics",
        f"- **Coverage**: {retrieval_coverage*100:.1f}%",
        f"- **Proxy Intent Hit Rate**: {proxy_hit_rate*100:.1f}%\n",
        "## Pipeline Metrics",
        f"- **Auto-Handle Rate**: {auto_handle_rate*100:.1f}% ({auto_handle_count})",
        f"- **Escalation Rate**: {escalation_rate*100:.1f}% ({escalation_count})\n"
    ]
    
    md_lines.append("## Representative Examples\n")
    # Show 5 auto-handled
    md_lines.append("### Successfully Auto-Handled\n")
    handled = [r for r in results_output if r['decision'] == 'AUTO_HANDLE'][:5]
    for r in handled:
        md_lines.append(f"**ID**: {r['example_id']}")
        md_lines.append(f"- **Message**: {r['customer_message']}")
        md_lines.append(f"- **Intent**: {r['predicted_intent']}")
        md_lines.append(f"- **Draft**: {r['draft_reply']}\n")
        
    # Show 5 escalations
    md_lines.append("### Escalated to Human\n")
    escalated = [r for r in results_output if r['decision'] == 'HUMAN_ESCALATION'][:5]
    for r in escalated:
        md_lines.append(f"**ID**: {r['example_id']}")
        md_lines.append(f"- **Message**: {r['customer_message']}")
        md_lines.append(f"- **Intent**: {r['predicted_intent']}")
        md_lines.append(f"- **Reason**: {r['escalation_reason']}\n")
        
    md_lines.append("## Limitations")
    md_lines.append("- The draft replies are purely deterministic extractions and are not evaluated for stylistic or contextual accuracy.")
    md_lines.append("- The retrieval proxy hit rate evaluates the top-1 result only.")
    md_lines.append("- No fabricated human/LLM agreement scores are included, as they are not yet supported by an active LLM.\n")
    
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    with open(reports_dir / "agent_evaluation.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    with open(reports_dir / "agent_evaluation.json", "w", encoding="utf-8") as f:
        json.dump({
            "metrics": {
                "intent_accuracy": intent_metrics.get('accuracy', 0),
                "intent_macro_f1": intent_metrics.get('macro_f1', 0),
                "retrieval_coverage": retrieval_coverage,
                "proxy_hit_rate": proxy_hit_rate,
                "auto_handle_rate": auto_handle_rate,
                "escalation_rate": escalation_rate
            },
            "examples": results_output
        }, f, indent=2)
        
    print(f"\nEvaluation Complete! Reports saved to {reports_dir}")

if __name__ == "__main__":
    main()
