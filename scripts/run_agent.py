import argparse
import json
from src.agent.agent import SupportAgent

def main():
    parser = argparse.ArgumentParser(description="Run the AppleSupport Agent Pipeline.")
    parser.add_argument("--message", type=str, required=True, help="Customer message to process.")
    parser.add_argument("--conversation_id", type=str, default=None, help="Optional conversation ID to exclude from retrieval.")
    args = parser.parse_args()

    print("\nLoading Support Agent components...")
    agent = SupportAgent()
    
    print(f"\nProcessing Message: \"{args.message}\"\n")
    
    result = agent.run(
        customer_message=args.message,
        conversation_id=args.conversation_id
    )
    
    print("=" * 50)
    print("AGENT RESULT")
    print("=" * 50)
    print(f"INTENT:             {result.intent}")
    print(f"DECISION:           {result.decision.value}")
    
    if result.escalation_reason:
        print(f"ESCALATION REASON:  {result.escalation_reason}")
        
    print("-" * 50)
    print("HISTORICAL EVIDENCE")
    if result.evidence:
        top_ev = result.evidence[0]
        print(f"Top Similarity:     {top_ev['similarity_score']:.3f}")
        print(f"Historical Issue:   {top_ev['customer_message']}")
        print(f"Historical Support: {top_ev['support_response']}")
    else:
        print("None retrieved.")
        
    print("-" * 50)
    print("DRAFT REPLY")
    print(result.draft_reply if result.draft_reply else "None (Escalated)")
    print("=" * 50)

if __name__ == "__main__":
    main()
