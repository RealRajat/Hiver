import pandas as pd
import numpy as np
from pathlib import Path
from typing import Union

def profile_brands(filepath: Union[str, Path]) -> pd.DataFrame:
    """
    Profiles support accounts (brands) from the TWCS dataset.
    Loads only necessary columns to remain memory-conscious (~300MB RAM for 3M rows).
    Includes deterministic conversation threading based on in_response_to_tweet_id.
    
    Args:
        filepath: Path to the TWCS CSV dataset.
        
    Returns:
        DataFrame containing metrics per candidate brand.
    """
    usecols = [
        'tweet_id', 'author_id', 'inbound',
        'response_tweet_id', 'in_response_to_tweet_id'
    ]
    df = pd.read_csv(filepath, usecols=usecols, low_memory=False)
    
    # Robustly parse inbound as boolean
    df['inbound'] = df['inbound'].astype(str).str.lower().isin(['true', '1'])
    
    # Ensure types for thread resolution
    df['tweet_id'] = df['tweet_id'].astype(str)
    df['in_response_to_tweet_id'] = pd.to_numeric(df['in_response_to_tweet_id'], errors='coerce').astype('Int64').astype(str)
    df['in_response_to_tweet_id'] = df['in_response_to_tweet_id'].replace('<NA>', np.nan)
    
    # Build conversation thread IDs
    parent_map = df.dropna(subset=['in_response_to_tweet_id']).set_index('tweet_id')['in_response_to_tweet_id'].to_dict()
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
    
    # 1. Identify candidates: Authors of at least one outbound tweet
    outbound_df = df[~df['inbound']]
    brand_authors = set(outbound_df['author_id'].dropna().unique())
    
    # Calculate Outbound Tweets per brand
    outbound_counts = outbound_df['author_id'].value_counts().rename('outbound_tweets')
    
    # 2. Relational Mapping for Interactions (Unique Customers & Inbound Tweets)
    tweet_to_author = df.set_index('tweet_id')['author_id'].to_dict()
    df['parent_author'] = df['in_response_to_tweet_id'].map(tweet_to_author)
    
    brand_replies = df[(~df['inbound']) & (df['parent_author'].notna())]
    customers_from_brand_replies = brand_replies.groupby('author_id')['parent_author'].agg(set)
    
    customer_replies = df[(df['inbound']) & (df['parent_author'].isin(brand_authors))]
    customers_from_customer_replies = customer_replies.groupby('parent_author')['author_id'].agg(set)
    
    inbound_counts = customer_replies.groupby('parent_author').size().rename('inbound_tweets')
    
    # Combine sets to get unique customers
    unique_customers = {}
    for brand in brand_authors:
        c1 = customers_from_brand_replies.get(brand, set())
        c2 = customers_from_customer_replies.get(brand, set())
        unique_customers[brand] = len(c1.union(c2))
        
    unique_customers_s = pd.Series(unique_customers, name='unique_customers')
    
    # 3. Conversation Metrics
    # Filter dataset to only conversations involving at least one brand tweet
    brand_convs = df[df['author_id'].isin(brand_authors)].groupby('author_id')['conversation_id'].agg(set)
    
    # Pre-calculate metrics for ALL conversations to avoid redundant grouping
    conv_sizes = df.groupby('conversation_id').size()
    conv_has_customer = df.groupby('conversation_id')['inbound'].any()
    conv_has_brand = df.groupby('conversation_id')['inbound'].apply(lambda x: (~x).any())
    conv_is_both = conv_has_customer & conv_has_brand
    
    # Build metrics per brand
    conv_counts = {}
    multi_turn = {}
    avg_len = {}
    med_len = {}
    cust_support_participation = {}
    
    for brand, c_ids in brand_convs.items():
        c_ids = list(c_ids)
        sizes = conv_sizes.loc[c_ids]
        conv_counts[brand] = len(sizes)
        multi_turn[brand] = (sizes > 1).sum()
        avg_len[brand] = sizes.mean()
        med_len[brand] = sizes.median()
        cust_support_participation[brand] = conv_is_both.loc[c_ids].sum()
        
    metrics_df = pd.DataFrame({
        'conversation_count': pd.Series(conv_counts),
        'multi_turn_conversations': pd.Series(multi_turn),
        'avg_conversation_length': pd.Series(avg_len).round(2),
        'median_conversation_length': pd.Series(med_len).round(2),
        'cust_support_participating_convs': pd.Series(cust_support_participation)
    })
    metrics_df['multi_turn_rate'] = (metrics_df['multi_turn_conversations'] / metrics_df['conversation_count']).fillna(0).round(4)
    metrics_df['participation_rate'] = (metrics_df['cust_support_participating_convs'] / metrics_df['conversation_count']).fillna(0).round(4)
    
    # 4. Compile the final dataframe
    profile_df = pd.DataFrame(index=list(brand_authors))
    profile_df.index.name = 'support_account'
    
    profile_df = profile_df.join(outbound_counts).join(inbound_counts).join(unique_customers_s).join(metrics_df)
    profile_df.fillna(0, inplace=True)
    
    profile_df['total_tweets'] = profile_df['outbound_tweets'] + profile_df['inbound_tweets']
    
    # Ensure types are integers for count columns
    int_cols = [
        'outbound_tweets', 'inbound_tweets', 'unique_customers', 'total_tweets', 
        'conversation_count', 'multi_turn_conversations', 'cust_support_participating_convs'
    ]
    for col in int_cols:
        profile_df[col] = profile_df[col].astype(int)
    
    # Reorder columns
    ordered_cols = [
        'total_tweets', 'inbound_tweets', 'outbound_tweets', 'unique_customers',
        'conversation_count', 'multi_turn_conversations', 'multi_turn_rate',
        'avg_conversation_length', 'median_conversation_length',
        'cust_support_participating_convs', 'participation_rate'
    ]
    profile_df = profile_df[ordered_cols]
    
    # Sort by total_tweets descending to surface strongest candidates
    profile_df = profile_df.sort_values(by='total_tweets', ascending=False).reset_index()
    
    return profile_df
