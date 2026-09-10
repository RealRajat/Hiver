# Brand Profiling Report

## Methodology
Candidate support accounts were identified heuristically by locating all `author_id`s that authored at least one outbound tweet (`inbound == False`). 

## Dataset Scope
The profiling used the full provided dataset, loaded memory-consciously by extracting only the relational and identification columns (`tweet_id`, `author_id`, `inbound`, `in_response_to_tweet_id`).

## Conversation Methodology
An identifiable conversation/thread is determined deterministically by resolving the `in_response_to_tweet_id` graph. Every tweet's parent path is traversed to find its root tweet. All tweets sharing the same root are grouped into a single conversation.

## Metrics
- **total_tweets**: Sum of inbound customer tweets directed at the brand and outbound replies from the brand.
- **inbound_tweets**: Number of customer tweets (`inbound == True`) that replied directly to the brand's tweets.
- **outbound_tweets**: Number of support tweets (`inbound == False`) authored by the brand.
- **unique_customers**: Number of distinct customer `author_id`s that either replied to the brand or were replied to by the brand.
- **conversation_count**: Number of identifiable conversation threads involving the support account.
- **multi_turn_conversations**: Threads containing more than one interaction/message.
- **multi_turn_rate**: Ratio of multi-turn conversations to total conversations.
- **avg_conversation_length**: Average number of messages per identifiable conversation.
- **cust_support_participating_convs**: Conversations containing both a customer message (`inbound == True`) and a support message (`inbound == False`).

## Candidate Comparison (Top 10 by Volume)

| support_account   |   total_tweets |   inbound_tweets |   outbound_tweets |   unique_customers |   conversation_count |   multi_turn_conversations |   multi_turn_rate |   avg_conversation_length |   median_conversation_length |   cust_support_participating_convs |   participation_rate |
|:------------------|---------------:|-----------------:|------------------:|-------------------:|---------------------:|---------------------------:|------------------:|--------------------------:|-----------------------------:|-----------------------------------:|---------------------:|
| AmazonHelp        |         270343 |           100503 |            169840 |              71668 |                82534 |                      82534 |                 1 |                      4.53 |                            3 |                              82534 |               1      |
| AppleSupport      |         143518 |            36658 |            106860 |              77432 |                80702 |                      80702 |                 1 |                      2.96 |                            2 |                              80702 |               1      |
| Uber_Support      |          78430 |            22160 |             56270 |              38951 |                41923 |                      41923 |                 1 |                      3.07 |                            2 |                              41923 |               1      |
| SpotifyCares      |          58361 |            15096 |             43265 |              27995 |                28280 |                      28280 |                 1 |                      3.25 |                            2 |                              28277 |               0.9999 |
| Delta             |          56723 |            14470 |             42253 |              22770 |                26166 |                      26166 |                 1 |                      3.36 |                            2 |                              26164 |               0.9999 |
| AmericanAir       |          54809 |            18045 |             36764 |              22433 |                26385 |                      26385 |                 1 |                      3.32 |                            2 |                              26385 |               1      |
| Tesco             |          51385 |            12812 |             38573 |              16010 |                16721 |                      16721 |                 1 |                      4.38 |                            4 |                              16721 |               1      |
| VirginTrains      |          46267 |            18450 |             27817 |              12996 |                14850 |                      14850 |                 1 |                      4.43 |                            3 |                              14848 |               0.9999 |
| TMobileHelp       |          45979 |            11662 |             34317 |              20145 |                22789 |                      22789 |                 1 |                      3.63 |                            2 |                              22789 |               1      |
| comcastcares      |          41937 |             8906 |             33031 |              22248 |                24061 |                      24061 |                 1 |                      3.04 |                            2 |                              24061 |               1      |

## Limitations
- **Lack of explicit brand labels**: Brands are inferred strictly from outbound behavior.
- **Incomplete conversation references**: Tweets that lack a valid `in_response_to_tweet_id` cannot be reliably linked to a customer/brand interaction.
- **Identifiable vs Real-World**: These metrics reflect *identifiable dataset threads*, not guaranteed real-world support cases. The dataset contains deleted parent tweets, unthreaded mentions, and missing context that naturally break conversations into smaller disjoint fragments.

## Reproducibility
```bash
python scripts/profile_brands.py --data-path data/raw/twcs.csv --output-dir reports
```
