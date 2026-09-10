import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union, List, Dict, Any

def reconstruct_brand_conversations(filepath: Union[str, Path], target_brand: str) -> List[Dict[str, Any]]:
    """
    Reconstructs all chronological conversation threads involving a specific target brand.
    Extracts the full text without loading the entire 3M row text column into memory at once.
    
    Args:
        filepath: Path to the raw TWCS dataset.
        target_brand: The support account to filter for (e.g., 'AppleSupport').
        
    Returns:
        List of conversation objects containing metadata and chronologically ordered messages.
    """
    # PASS 1: Build the relational graph using only structural columns to conserve memory
    usecols_pass1 = [
        'tweet_id', 'author_id', 'inbound', 'in_response_to_tweet_id'
    ]
    df_graph = pd.read_csv(filepath, usecols=usecols_pass1, low_memory=False)
    
    df_graph['tweet_id'] = df_graph['tweet_id'].astype(str)
    df_graph['in_response_to_tweet_id'] = pd.to_numeric(df_graph['in_response_to_tweet_id'], errors='coerce').astype('Int64').astype(str)
    df_graph['in_response_to_tweet_id'] = df_graph['in_response_to_tweet_id'].replace('<NA>', np.nan)
    
    # Root resolution logic (deterministic)
    parent_map = df_graph.dropna(subset=['in_response_to_tweet_id']).set_index('tweet_id')['in_response_to_tweet_id'].to_dict()
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
            if curr in path:
                curr = path[0] # Break cycle arbitrarily to prevent infinite loop
                break
        for node in path:
            roots[node] = curr
        return curr
        
    df_graph['conversation_id'] = df_graph['tweet_id'].apply(get_root)
    
    # Identify conversations containing at least one tweet authored by the target brand
    brand_tweets = df_graph[df_graph['author_id'] == target_brand]
    target_conv_ids = set(brand_tweets['conversation_id'])
    
    # Identify the specific tweet IDs that belong to these conversations
    target_tweet_ids = set(df_graph[df_graph['conversation_id'].isin(target_conv_ids)]['tweet_id'])
    
    # Pre-cache conversation root mappings so we don't need to compute them again
    tweet_to_conv = df_graph[df_graph['tweet_id'].isin(target_tweet_ids)].set_index('tweet_id')['conversation_id'].to_dict()
    
    # Delete the graph to free memory
    del df_graph
    
    # PASS 2: Load the full data for ONLY the target tweets in chunks
    chunks = pd.read_csv(filepath, low_memory=False, chunksize=100000)
    filtered_chunks = []
    
    for chunk in chunks:
        chunk['tweet_id'] = chunk['tweet_id'].astype(str)
        matched = chunk[chunk['tweet_id'].isin(target_tweet_ids)].copy()
        if not matched.empty:
            filtered_chunks.append(matched)
            
    if not filtered_chunks:
        return []
        
    df_target = pd.concat(filtered_chunks, ignore_index=True)
    
    # Robust data cleaning
    df_target['inbound'] = df_target['inbound'].astype(str).str.lower().isin(['true', '1'])
    # Parse dates
    df_target['created_at_dt'] = pd.to_datetime(df_target['created_at'], format='%a %b %d %H:%M:%S +0000 %Y', errors='coerce')
    
    # Map back conversation_ids
    df_target['conversation_id'] = df_target['tweet_id'].map(tweet_to_conv)
    
    # Assembly: Group by conversation_id and sort chronologically
    conversations = []
    
    grouped = df_target.groupby('conversation_id')
    for conv_id, group in grouped:
        # Sort chronologically
        group = group.sort_values(by='created_at_dt', na_position='first')
        
        # Prepare messages
        messages_df = group.drop(columns=['created_at_dt'])
        messages = messages_df.to_dict(orient='records')
        
        # Clean NaNs for JSON serialization
        for msg in messages:
            for k, v in msg.items():
                if isinstance(v, float) and pd.isna(v):
                    msg[k] = None
        
        # Metadata
        tweet_count = len(messages)
        customer_msgs = sum(1 for m in messages if m['inbound'])
        support_msgs = sum(1 for m in messages if not m['inbound'])
        
        # Calculate bounds from parsed datetimes
        valid_dates = group['created_at_dt'].dropna()
        start_time = valid_dates.min().strftime('%Y-%m-%dT%H:%M:%S') if not valid_dates.empty else None
        end_time = valid_dates.max().strftime('%Y-%m-%dT%H:%M:%S') if not valid_dates.empty else None
        
        conv_obj = {
            'conversation_id': str(conv_id),
            'tweet_count': tweet_count,
            'customer_message_count': customer_msgs,
            'support_message_count': support_msgs,
            'has_customer': customer_msgs > 0,
            'has_support': support_msgs > 0,
            'start_time': start_time,
            'end_time': end_time,
            'messages': messages
        }
        conversations.append(conv_obj)
        
    return conversations
