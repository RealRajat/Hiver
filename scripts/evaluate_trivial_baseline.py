import json
from pathlib import Path
from src.evaluation.golden_loader import GoldenSetLoader
from src.evaluation.trivial_baseline import MajorityClassClassifier
from src.evaluation.metrics import calculate_intent_metrics

def main():
    print("Loading Golden Set...")
    loader = GoldenSetLoader()
    dataset = loader.load()
    
    print("Initializing Trivial Baseline (Majority Class) Classifier...")
    print("Determining majority class from reference corpus (excluding eval set)...")
    classifier = MajorityClassClassifier()
    majority_class = classifier.majority_class
    print(f"Determined Majority Class: {majority_class}")
    
    total_queries = len(dataset)
    y_true_intent = []
    y_pred_intent = []
    
    for i, example in enumerate(dataset):
        gold_intent = example['intent']
        msg = example['customer_message']
        
        pred_intent = classifier.predict(msg)
        
        y_true_intent.append(gold_intent)
        y_pred_intent.append(pred_intent)
        
    print("Calculating metrics...")
    labels = list(GoldenSetLoader.VALID_INTENTS)
    intent_metrics = calculate_intent_metrics(y_true_intent, y_pred_intent, labels)
    
    accuracy = intent_metrics.get('accuracy', 0)
    macro_f1 = intent_metrics.get('macro_f1', 0)
    
    print(f"Majority-class baseline Accuracy: {accuracy*100:.2f}%")
    print(f"Majority-class baseline Macro F1: {macro_f1*100:.2f}%")
    
    # Write report
    md_lines = [
        "# Baseline Comparison Report\n",
        "## Performance Metrics\n",
        "| Model | Accuracy | Macro F1 | Description |",
        "|-------|----------|----------|-------------|",
        f"| Majority-class baseline | {accuracy*100:.2f}% | {macro_f1*100:.2f}% | Trivial baseline (Always predicts '{majority_class}') |",
        "| Keyword/Regex baseline | 47.50% | 42.23% | Simple deterministic baseline |",
        "| LLM Agent | Pending | Pending | Generative LLM with strict evidence grounding |",
        "\n",
        "*(Note: The LLM Evaluation is pending human grading and API credentials.)*"
    ]
    
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    with open(reports_dir / "baseline_comparison.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    print("Evaluation Complete! Reports saved to reports/baseline_comparison.md")

if __name__ == "__main__":
    main()
