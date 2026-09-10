from typing import List, Dict, Any, Optional
from src.retrieval.models import BaseRetriever
from src.retrieval.resolution_pairs import ResolutionPairExtractor

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
except ImportError:
    raise ImportError("scikit-learn is required for LexicalRetriever.")

class LexicalRetriever(BaseRetriever):
    """
    Deterministic TF-IDF based lexical retriever.
    """
    def __init__(self, pairs: Optional[List[Dict[str, Any]]] = None):
        self.pairs = pairs if pairs is not None else ResolutionPairExtractor().extract_pairs()
        
        corpus_texts = [p['customer_message'] for p in self.pairs]
        if not corpus_texts:
            self.tfidf_matrix = None
        else:
            # Adjust parameters for extremely small test corpora
            min_df = 2 if len(corpus_texts) > 2 else 1
            max_df = 0.95 if len(corpus_texts) > 2 else 1.0
            self.vectorizer = TfidfVectorizer(stop_words='english', max_df=max_df, min_df=min_df)
            self.tfidf_matrix = self.vectorizer.fit_transform(corpus_texts)
            
    def search(self, query: str, top_k: int = 5, exclude_conversation_ids: Optional[List[str]] = None) -> List[Dict[str, Any]]:
        if not self.tfidf_matrix is not None or not query.strip():
            return []
            
        exclude_ids = set(exclude_conversation_ids) if exclude_conversation_ids else set()
        
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.tfidf_matrix).flatten()
        
        # Build results
        results = []
        for idx, score in enumerate(similarities):
            # We enforce a tiny threshold to avoid returning purely empty/0.0 matches
            if score > 0.0:
                pair = self.pairs[idx]
                if pair['conversation_id'] not in exclude_ids:
                    results.append({
                        "conversation_id": pair['conversation_id'],
                        "customer_tweet_id": pair['customer_tweet_id'],
                        "customer_message": pair['customer_message'],
                        "support_response": pair['support_response'],
                        "similarity_score": float(score),
                        "retrieval_method": "tf-idf"
                    })
                    
        # Deterministic sort: similarity DESC, then conversation_id ASC to break ties
        results.sort(key=lambda x: (-x['similarity_score'], x['conversation_id']))
        
        return results[:top_k]
