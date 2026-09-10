import pytest
import pandas as pd
import tempfile
import os
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.conversations.conversation_reconstructor import reconstruct_brand_conversations

@pytest.fixture
def synthetic_twcs_fixture():
    # 1 brand, 2 customers, 5 tweets
    # Tweet 1: Customer tweets brand (root of Conv 1)
    # Tweet 2: Brand replies to Customer 1 (Conv 1)
    # Tweet 3: Customer 1 replies to Brand (Conv 1) -> 3 turn conversation
    # Tweet 4: Another brand outbound (no replies) (Conv 2) -> Not target brand
    # Tweet 5: Orphaned reply to non-existent tweet (Conv 3) -> 1 turn
    return pd.DataFrame({
        'tweet_id': ['1', '2', '3', '4', '5'],
        'author_id': ['Cust1', 'AppleSupport', 'Cust1', 'AmazonHelp', 'Cust2'],
        'inbound': [True, False, True, False, True],
        'created_at': [
            'Wed Oct 11 20:00:00 +0000 2017',
            'Wed Oct 11 20:05:00 +0000 2017',
            'Wed Oct 11 20:10:00 +0000 2017',
            'Wed Oct 11 20:15:00 +0000 2017',
            'Wed Oct 11 20:20:00 +0000 2017'
        ],
        'text': ['Help me', 'Ok', 'Thanks', 'Hello', 'Orphan'],
        'response_tweet_id': ['2', '3', None, None, None],
        'in_response_to_tweet_id': [None, '1', '2', None, '999']
    })

def test_conversation_reconstructor(synthetic_twcs_fixture):
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
        synthetic_twcs_fixture.to_csv(tmp.name, index=False)
        tmp_path = tmp.name

    try:
        conversations = reconstruct_brand_conversations(tmp_path, 'AppleSupport')
        
        # Only Conv 1 contains AppleSupport
        assert len(conversations) == 1
        
        conv = conversations[0]
        assert conv['conversation_id'] == '1'
        assert conv['tweet_count'] == 3
        assert conv['customer_message_count'] == 2
        assert conv['support_message_count'] == 1
        assert conv['has_customer'] is True
        assert conv['has_support'] is True
        
        msgs = conv['messages']
        assert len(msgs) == 3
        
        # Check chronological order
        assert msgs[0]['tweet_id'] == '1'
        assert msgs[1]['tweet_id'] == '2'
        assert msgs[2]['tweet_id'] == '3'
        
        # Check metadata
        assert msgs[1]['author_id'] == 'AppleSupport'
        assert msgs[1]['text'] == 'Ok'

    finally:
        os.remove(tmp_path)
