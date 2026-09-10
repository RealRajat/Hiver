import json
import statistics
from pathlib import Path
from src.evaluation.golden_loader import GoldenSetLoader
from src.evaluation.baseline_classifier import BaselineIntentClassifier
from src.retrieval.lexical_retriever import LexicalRetriever

def main():
    print("Loading Golden Set...")
    loader = GoldenSetLoader()
    dataset = loader.load()
    
    print("Building Lexical Retriever index from historical resolution pairs...")
    retriever = LexicalRetriever()
    classifier = BaselineIntentClassifier()
    
    total_queries = len(dataset)
    queries_with_results = 0
    all_top_k_similarities = []
    proxy_relevance_hits = 0
    
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    results_output = []
    md_lines = []
    
    md_lines.append("# Historical Evidence Retrieval Report\n")
    md_lines.append("## Methodology\n")
    md_lines.append("- **Retriever**: Deterministic TF-IDF + Cosine Similarity (Baseline)")
    md_lines.append("- **Leakage Prevention**: Exclusion by `conversation_id` enforced during search.")
    md_lines.append("- **Proxy Relevance Metric**: Percentage of queries where at least one retrieved result's customer message yields the same baseline-classified intent as the gold query. *(Note: This is a proxy measurement, not a genuine human relevance judgment.)*\n")
    
    md_lines.append("## Detailed Inspections\n")
    md_lines.append("Showing retrieval inspections for the first 20 examples:\n")
    
    for i, example in enumerate(dataset):
        query = example['customer_message']
        gold_intent = example['intent']
        conv_id = str(example['conversation_id'])
        
        # Search while preventing self-retrieval data leakage
        results = retriever.search(query, top_k=5, exclude_conversation_ids=[conv_id])
        
        if results:
            queries_with_results += 1
            avg_sim = sum(r['similarity_score'] for r in results) / len(results)
            all_top_k_similarities.append(avg_sim)
            
            # Proxy relevance: does any retrieved result match the gold intent?
            has_proxy_match = False
            for r in results:
                pred_intent = classifier.predict(r['customer_message'])
                r['proxy_intent'] = pred_intent
                if pred_intent == gold_intent:
                    has_proxy_match = True
                    
            if has_proxy_match:
                proxy_relevance_hits += 1
        else:
            avg_sim = 0.0
            
        # Store for JSON
        results_output.append({
            "example_id": example['example_id'],
            "customer_message": query,
            "gold_intent": gold_intent,
            "results_found": len(results),
            "results": results
        })
        
        # Markdown limit to 20
        if i < 20:
            md_lines.append(f"### Query: {example['example_id']}")
            md_lines.append(f"**Customer Message**: {query}")
            md_lines.append(f"**Gold Intent**: {gold_intent}")
            if not results:
                md_lines.append("*No results found.*\n")
            else:
                for j, r in enumerate(results, 1):
                    md_lines.append(f"  - **Result {j}** (Sim: {r['similarity_score']:.3f}, Proxy Intent: {r.get('proxy_intent')})")
                    md_lines.append(f"    - Issue: {r['customer_message']}")
                    md_lines.append(f"    - Resolution: {r['support_response']}")
            md_lines.append("\n")
            
    # Calculate stats
    coverage = queries_with_results / total_queries
    avg_top_k_sim = statistics.mean(all_top_k_similarities) if all_top_k_similarities else 0.0
    proxy_relevance_pct = proxy_relevance_hits / total_queries
    
    # Prepend stats
    stats_lines = [
        "## Summary Metrics\n",
        f"- **Queries Processed**: {total_queries}",
        f"- **Queries with ≥1 Result**: {queries_with_results} ({coverage*100:.1f}%)",
        f"- **Average Top-K Similarity**: {avg_top_k_sim:.4f}",
        f"- **Proxy Relevance Hit Rate**: {proxy_relevance_pct*100:.1f}%\n"
    ]
    md_lines = md_lines[:6] + stats_lines + md_lines[6:]
    
    with open(reports_dir / "retrieval_results.md", "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))
        
    with open(reports_dir / "retrieval_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "metrics": {
                "total_queries": total_queries,
                "coverage_pct": coverage,
                "avg_top_k_similarity": avg_top_k_sim,
                "proxy_relevance_hit_rate": proxy_relevance_pct
            },
            "inspections": results_output
        }, f, indent=2)
        
    print(f"Retrieval evaluation complete. Saved to {reports_dir}")

if __name__ == "__main__":
    main()
