import pandas as pd
import time
import numpy as np

def test_conversations():
    start = time.time()
    usecols = ['tweet_id', 'author_id', 'inbound', 'in_response_to_tweet_id']
    df = pd.read_csv('data/raw/twcs.csv', usecols=usecols, low_memory=False)
    print(f"Loaded in {time.time() - start:.2f}s")
    
    start = time.time()
    # Handle NaNs and types
    df['tweet_id'] = df['tweet_id'].astype(str)
    # in_response_to_tweet_id is float if NaNs exist. 
    # Pandas float string conversion: "1.0" instead of "1". We must handle this.
    # Convert to numeric, then Int64 (nullable int), then string
    df['in_response_to_tweet_id'] = pd.to_numeric(df['in_response_to_tweet_id'], errors='coerce').astype('Int64').astype(str)
    # 'nan' comes from Int64 to str
    df['in_response_to_tweet_id'] = df['in_response_to_tweet_id'].replace('<NA>', np.nan)
    
    parent_map = df.dropna(subset=['in_response_to_tweet_id']).set_index('tweet_id')['in_response_to_tweet_id'].to_dict()
    
    # Pre-allocate array for roots
    roots = {}
    
    def get_root(tid):
        if tid in roots:
            return roots[tid]
        curr = tid
        path = []
        while curr in parent_map:
            path.append(curr)
            curr = parent_map[curr]
            if curr in roots:
                curr = roots[curr]
                break
            if curr in path: # Cycle detected
                curr = path[0] # Break arbitrarily
                break
        for node in path:
            roots[node] = curr
        return curr

    df['conversation_id'] = df['tweet_id'].apply(get_root)
    print(f"Resolved roots in {time.time() - start:.2f}s")
    
    start = time.time()
    print(f"Total distinct conversations: {df['conversation_id'].nunique()}")
    
    # Filter for AmazonHelp
    amazon_tweets = df[df['author_id'] == 'AmazonHelp']
    # Conversations involving AmazonHelp
    amazon_convs = df[df['conversation_id'].isin(amazon_tweets['conversation_id'])]
    
    conv_sizes = amazon_convs.groupby('conversation_id').size()
    print(f"AmazonHelp - Total Conversations: {len(conv_sizes)}")
    print(f"AmazonHelp - Multi-turn: {(conv_sizes > 1).sum()}")
    print(f"AmazonHelp - Avg length: {conv_sizes.mean():.2f}")
    
    print(f"Stats calculated in {time.time() - start:.2f}s")

if __name__ == "__main__":
    test_conversations()
