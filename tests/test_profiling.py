import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.profiling.brand_profiler import profile_brands

@pytest.fixture
def synthetic_twcs_fixture():
    # 1 brand, 2 customers, 5 tweets
    # Tweet 1: Customer tweets brand (root of Conv 1)
    # Tweet 2: Brand replies to Customer 1 (Conv 1)
    # Tweet 3: Customer 1 replies to Brand (Conv 1) -> 3 turn conversation
    # Tweet 4: Another brand outbound (no replies) (Conv 2) -> 1 turn conversation
    # Tweet 5: Orphaned reply to non-existent tweet (Conv 3) -> 1 turn
    return pd.DataFrame({
        'tweet_id': ['1', '2', '3', '4', '5'],
        'author_id': ['Cust1', 'BrandA', 'Cust1', 'BrandB', 'Cust2'],
        'inbound': [True, False, True, False, True],
        'created_at': ['2023-01-01'] * 5,
        'response_tweet_id': ['2', '3', None, None, None],
        'in_response_to_tweet_id': [None, '1', '2', None, '999']
    })

def test_brand_profiler_metrics(synthetic_twcs_fixture):
    # Write synthetic data to temp file
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        synthetic_twcs_fixture.to_csv(tmp.name, index=False)
        tmp_path = tmp.name

    try:
        df_profile = profile_brands(tmp_path)
        
        # Verify 2 candidates found
        assert len(df_profile) == 2
        
        # Check BrandA metrics
        brand_a = df_profile[df_profile['support_account'] == 'BrandA'].iloc[0]
        assert brand_a['outbound_tweets'] == 1
        assert brand_a['inbound_tweets'] == 1 # Cust1 replies to BrandA in Tweet 3
        assert brand_a['unique_customers'] == 1
        assert brand_a['total_tweets'] == 2 # 1 outbound, 1 inbound directed at brand
        assert brand_a['conversation_count'] == 1
        assert brand_a['multi_turn_conversations'] == 1
        assert brand_a['avg_conversation_length'] == 3.0 # Tweets 1, 2, 3
        assert brand_a['cust_support_participating_convs'] == 1
        
        # Check BrandB metrics
        brand_b = df_profile[df_profile['support_account'] == 'BrandB'].iloc[0]
        assert brand_b['outbound_tweets'] == 1
        assert brand_b['inbound_tweets'] == 0
        assert brand_b['unique_customers'] == 0
        assert brand_b['conversation_count'] == 1
        assert brand_b['multi_turn_conversations'] == 0
        assert brand_b['avg_conversation_length'] == 1.0

    finally:
        os.remove(tmp_path)
