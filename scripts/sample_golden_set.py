import json
import random
import csv
from pathlib import Path

def main():
    jsonl_path = Path("data/processed/applesupport_conversations.jsonl")
    if not jsonl_path.exists():
        print("Corpus not found.")
        return
        
    # 1. Load and filter valid first customer messages
    candidates = []
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            conv = json.loads(line)
            # Find the first customer message
            for msg in conv.get("messages", []):
                if msg.get("inbound") == True:
                    text = msg.get("text", "")
                    if len(text.strip()) > 10: # Avoid tiny noise
                        candidates.append({
                            'conversation_id': conv['conversation_id'],
                            'tweet_id': msg['tweet_id'],
                            'text': text
                        })
                    break
                    
    # 2. Reproducible Sampling
    random.seed(42)
    sample = random.sample(candidates, 200)
    
    # 3. Queue Preparation (NO AUTOMATED LABELS)
    annotation_queue = []
    
    for i, item in enumerate(sample):
        annotation_queue.append({
            'example_id': f'GOLDEN_{i+1:03d}',
            'conversation_id': item['conversation_id'],
            'tweet_id': item['tweet_id'],
            'customer_message': item['text'].replace('\n', ' '),
            'optional_context': '',
            'annotation_status': 'unreviewed',
            'intent': '',
            'ambiguity_flag': '',
            'annotation_notes': ''
        })
        
    # 4. Export Annotation Queue CSV
    output_path = Path("data/evaluation/golden_annotation_queue.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    headers = ['example_id', 'conversation_id', 'tweet_id', 'customer_message', 
               'optional_context', 'annotation_status', 'intent', 'ambiguity_flag', 'annotation_notes']
               
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(annotation_queue)
        
    # 5. Generate Sampling Report Data
    report_content = f"""# Golden Set Sampling Report

## Sampling Method
- **Source Corpus**: `data/processed/applesupport_conversations.jsonl`
- **Sampling Strategy**: Random sample of the first customer message using a fixed random seed (`seed=42`).
- **Exclusions**: Messages shorter than 10 characters were excluded to filter out tiny noise (e.g., "hi").
- **Candidate Population**: {len(candidates)} valid first-customer messages.
- **Final Sample Size**: {len(annotation_queue)} examples placed in the queue.

## Annotation Workflow
The 200 examples have been exported to `data/evaluation/golden_annotation_queue.csv` for manual human review.
- **Automated Labels**: Discarded. No LLM or heuristic was used to generate intent labels.
- **Status**: Currently pending human annotation.

## Intent Distribution
*(Pending human annotation)*

## Ambiguity
*(Pending human annotation)*
"""

    report_path = Path("reports/golden_set_sampling.md")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print(f"Annotation queue created: {output_path}")
    print(f"Sampling report updated: {report_path}")

if __name__ == "__main__":
    main()
