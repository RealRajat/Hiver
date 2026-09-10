import json
import random
from collections import Counter
import re
from pathlib import Path

def get_ngrams(text, n=2):
    # simple tokenization
    words = re.findall(r'\b[a-z]{3,}\b', text.lower())
    # remove common stop words loosely
    stop_words = {'the', 'and', 'for', 'that', 'you', 'with', 'have', 'this', 'but', 'not', 'are', 'was', 'can', 'my', 'is', 'it', 'on', 'in', 'to', 'of', 'i', 'a', 'it', 'me', 'so', 'just', 'like', 'how', 'do', 'what'}
    words = [w for w in words if w not in stop_words]
    ngrams = zip(*[words[i:] for i in range(n)])
    return [" ".join(ngram) for ngram in ngrams]

def main():
    jsonl_path = Path("data/processed/applesupport_conversations.jsonl")
    if not jsonl_path.exists():
        print("Corpus not found.")
        return
        
    random.seed(42)
    
    first_customer_messages = []
    
    with open(jsonl_path, 'r', encoding='utf-8') as f:
        for line in f:
            conv = json.loads(line)
            # Find the first customer message
            for msg in conv.get("messages", []):
                if msg.get("inbound") == True:
                    text = msg.get("text", "")
                    # Clean out @AppleSupport handles for better keyword frequency
                    text_clean = re.sub(r'@\w+', '', text).strip()
                    first_customer_messages.append(text_clean)
                    break # Only take the first one per conversation
                    
    print(f"Extracted {len(first_customer_messages)} first-customer messages.")
    
    # 1. Bigram Analysis
    all_bigrams = []
    for msg in first_customer_messages:
        all_bigrams.extend(get_ngrams(msg, 2))
        
    top_bigrams = Counter(all_bigrams).most_common(30)
    sample_size = 50
    sample = random.sample(first_customer_messages, sample_size)
    
    with open("reports/intent_sample.txt", "w", encoding="utf-8") as out_f:
        out_f.write(f"--- Top 30 Bigrams ---\n")
        for bg, count in top_bigrams:
            out_f.write(f"{bg}: {count}\n")
            
        out_f.write(f"\n--- Random Sample ({sample_size} messages) ---\n")
        for i, msg in enumerate(sample, 1):
            safe_msg = msg.replace("\n", " ")
            out_f.write(f"{i}. {safe_msg}\n")
    print("Sample written to reports/intent_sample.txt")

if __name__ == "__main__":
    main()
