import json
from pathlib import Path
from src.evaluation.golden_loader import GoldenSetLoader
from src.evaluation.baseline_classifier import BaselineIntentClassifier
from src.evaluation.metrics import calculate_intent_metrics

def main():
    print("Loading Evaluation Harness...")
    loader = GoldenSetLoader()
    try:
        dataset = loader.load()
    except Exception as e:
        print(f"Error loading golden set: {e}")
        return
        
    classifier = BaselineIntentClassifier()
    labels = list(GoldenSetLoader.VALID_INTENTS)
    
    # 1. Run Predictions
    y_true_all = []
    y_pred_all = []
    errors = []
    
    ambiguous_indices = []
    unambiguous_indices = []
    
    for i, example in enumerate(dataset):
        gold = example['intent']
        pred = classifier.predict(example['customer_message'])
        
        y_true_all.append(gold)
        y_pred_all.append(pred)
        
        is_ambig = str(example['ambiguity_flag']).lower() == 'true'
        if is_ambig:
            ambiguous_indices.append(i)
        else:
            unambiguous_indices.append(i)
            
        if gold != pred:
            errors.append({
                'example_id': example['example_id'],
                'customer_message': example['customer_message'],
                'gold_intent': gold,
                'predicted_intent': pred,
                'ambiguity_flag': is_ambig,
                'annotation_notes': example.get('annotation_notes', '')
            })
            
    # 2. Calculate Metrics
    metrics_all = calculate_intent_metrics(y_true_all, y_pred_all, labels)
    
    y_true_ambig = [y_true_all[i] for i in ambiguous_indices]
    y_pred_ambig = [y_pred_all[i] for i in ambiguous_indices]
    metrics_ambig = calculate_intent_metrics(y_true_ambig, y_pred_ambig, labels)
    
    y_true_unambig = [y_true_all[i] for i in unambiguous_indices]
    y_pred_unambig = [y_pred_all[i] for i in unambiguous_indices]
    metrics_unambig = calculate_intent_metrics(y_true_unambig, y_pred_unambig, labels)
    
    # 3. Format Output
    output_data = {
        'dataset_size': len(dataset),
        'metrics_overall': metrics_all,
        'metrics_ambiguous_only': metrics_ambig,
        'metrics_unambiguous_only': metrics_unambig,
        'representative_errors': errors[:20]  # limit to 20 for brevity
    }
    
    # Save JSON
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    with open(reports_dir / "baseline_intent_results.json", "w", encoding='utf-8') as f:
        json.dump(output_data, f, indent=2)
        
    # Save Markdown
    md_content = f"""# Baseline Intent Evaluation Report

## Dataset
- **Size**: {len(dataset)} examples
- **Unambiguous**: {len(unambiguous_indices)}
- **Ambiguous**: {len(ambiguous_indices)}

## Overall Metrics
- **Accuracy**: {metrics_all.get('accuracy', 0):.4f}
- **Macro F1**: {metrics_all.get('macro_f1', 0):.4f}
- **Macro Precision**: {metrics_all.get('macro_precision', 0):.4f}
- **Macro Recall**: {metrics_all.get('macro_recall', 0):.4f}

## Ambiguity Split
- **Unambiguous Accuracy**: {metrics_unambig.get('accuracy', 0):.4f} (Macro F1: {metrics_unambig.get('macro_f1', 0):.4f})
- **Ambiguous Accuracy**: {metrics_ambig.get('accuracy', 0):.4f} (Macro F1: {metrics_ambig.get('macro_f1', 0):.4f})

## Representative Errors
Showing up to 20 mismatched examples:
"""
    for err in errors[:20]:
        md_content += f"""
### {err['example_id']}
**Message**: {err['customer_message']}
- **Gold**: {err['gold_intent']}
- **Predicted**: {err['predicted_intent']}
- **Ambiguous**: {err['ambiguity_flag']}
- **Notes**: {err['annotation_notes']}
"""
    with open(reports_dir / "baseline_intent_results.md", "w", encoding='utf-8') as f:
        f.write(md_content)
        
    print(f"Evaluation complete. Reports saved to {reports_dir}")

if __name__ == "__main__":
    main()
