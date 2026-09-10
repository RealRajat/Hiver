# AppleSupport Intent Discovery

## Objective
The objective of this phase is to discover a small, useful, and cohesive set of customer-support intents based strictly on historical `AppleSupport` conversations. This taxonomy will serve as the classification schema for the final AI support agent, enabling it to route issues or retrieve relevant RAG knowledge based on the customer's initial message.

## Sampling Method
A reproducible sampling utility (`scripts/discover_intents.py`) was used to:
1. Filter the `applesupport_conversations.jsonl` corpus for the *first customer message* of every conversation.
2. Tokenize and extract the Top 30 Bigrams across all 80,702 customer messages to observe dataset-wide themes.
3. Extract a random sample of 50 customer messages (using a fixed random seed) for manual qualitative review and grouping.

## Data Examined
- **Total Conversations Analyzed**: 80,702 (Bigram extraction)
- **Random Sample Reviewed**: 50 customer messages
- **Date/Context**: The data strongly reflects the iOS 11 launch window (late 2017), dominated by specific update bugs (e.g., the infamous `I` -> `?` typing bug).

## Observed Themes
The bigram analysis revealed immense volume around:
- **Updates**: `ios update` (2,107), `new update` (1,783)
- **Bugs/Glitches**: `please fix` (2,040), `question mark` (1,462)
- **Hardware/Performance**: `battery life` (1,505), `phone keeps` (628)
- **Services**: `apple music` (936)

The qualitative sample confirmed that customer messages naturally cluster into distinct support tasks rather than product-specific silos (e.g., customers asked similar troubleshooting questions whether using an iPhone 7 or an iPhone X).

## Candidate Taxonomy

1. **Software Bug / Glitch**
2. **Device Performance / Hardware**
3. **Purchase & Store Operations**
4. **Services & Account**
5. **How-To / Feature Question**
6. **General Complaint / Venting**

---

## Intent Definitions & Representative Examples

### 1. Software Bug / Glitch
- **Definition**: The customer is reporting a specific unexpected behavior, UI anomaly, or software bug in iOS, macOS, or first-party apps.
- **Includes**: Feature bugs, connectivity glitches (WiFi/Bluetooth), UI alignment issues, unexpected errors.
- **Excludes**: Total device failure, battery drain, or physical damage.
- **Representative Examples**:
  - *"Yo I️ I️ I️ why does the letter I️ turn into a question mark in a box. Thanks."*
  - *"Hey is this a known bug that will be fixed soon? My dock on iPad continues to not stay centered"*
- **Agent Usefulness**: The agent can query RAG for known bugs/workarounds (like the iOS 11.1 typing bug fix).

### 2. Device Performance / Hardware
- **Definition**: The customer is reporting a core operational failure, battery issue, freezing, crashing, or physical hardware problem.
- **Includes**: Battery drain, phone won't turn on, physical damage, repair requests, device freezing/crashing.
- **Excludes**: Specific app bugs where the rest of the phone works fine.
- **Representative Examples**:
  - *"my iPhone 7 Plus keeps freezing, please send help"*
  - *"so my phone wont turn on and Apple isn't even helping me"*
- **Agent Usefulness**: The agent can trigger diagnostic flows, battery health checks, or offer to schedule a Genius Bar repair.

### 3. Purchase & Store Operations
- **Definition**: The customer is asking about buying products, order status, carrier activation, or physical retail store experiences.
- **Includes**: Order tracking, inventory questions, store appointments, upgrade programs.
- **Excludes**: App Store digital purchases (which belong in Services & Account).
- **Representative Examples**:
  - *"When trying to buy the iPhone X on Friday in store, is it possible to do an online store pickup?"*
  - *"had worst experience today at the Orlando store @ Millenia. Had Appt @ 4pm and waited until 5"*
- **Agent Usefulness**: The agent can route to the Sales/Retail team or ask for an Order Number.

### 4. Services & Account
- **Definition**: The customer is having an issue with an Apple digital service, subscription, Apple ID, or digital billing.
- **Includes**: Apple Music, iCloud storage, App Store downloads, Apple ID password resets, digital billing.
- **Excludes**: Buying physical hardware.
- **Representative Examples**:
  - *"I really hate how Apple Music works with having a family. Anytime more than one person in a family wants to listen it kicks the other off"*
  - *"haven't been able to use AppStore all day! Help! 😓"*
- **Agent Usefulness**: The agent can securely authenticate the user to check subscription status or server outages.

### 5. How-To / Feature Question
- **Definition**: The customer is asking for instructions on how to use a feature, without implying the feature is fundamentally broken.
- **Includes**: Setup assistance, "how do I...", settings configuration.
- **Excludes**: Reporting a bug.
- **Representative Examples**:
  - *"literally cannot figure out how to delete a movie off my phone for the life of me since the new update."*
  - *"battery indicator on my iPod seems inaccurate and I don't know what's the right way to calibrate it."*
- **Agent Usefulness**: The agent can directly retrieve and summarize step-by-step Apple Support documentation via RAG.

### 6. General Complaint / Venting (Other)
- **Definition**: The customer is expressing frustration or anger without providing a specific, actionable technical request or context.
- **Includes**: "Worst update ever", generic frustration, planned obsolescence complaints.
- **Excludes**: Complaints that contain a specific bug description (which should be routed to Software Bug).
- **Representative Examples**:
  - *"this is honestly the worst iOS update that has ever existed. Fix this ASAP."*
  - *"always messes up older version phones whenever the new one comes with their 'updates' 😂"*
- **Agent Usefulness**: The agent can provide an empathetic response and ask the user to specify exactly what behavior they are experiencing.

---

## Coverage
Based on the random sample of 50 messages, the proposed taxonomy covers **100%** of the sampled first-customer messages. 
- Software Bug/Glitch: ~36%
- Device Performance: ~18%
- General Complaint: ~16%
- Purchase/Store: ~12%
- How-To: ~10%
- Services/Account: ~8%

*(Note: These percentages are illustrative of the 50-message sample and heavily influenced by the iOS 11 release window).*

## Ambiguities & Difficult Cases
- **Bugs vs. Venting**: Many tweets complain about the OS update *while* venting (e.g., "fix the damn glitch already!"). If no specific glitch is named, it falls into *General Complaint*, requiring the agent to ask for clarification.
- **Device vs. Software**: "Phone keeps freezing" could be a hardware memory issue or a software iOS bug. We classify severe device-level usability issues as *Device Performance / Hardware* because the agent's response (running diagnostics) is the same regardless of the root cause.
- **Short Replies**: Messages like "still not working" lack context if the system isn't tracking previous interactions.

## Taxonomy Decisions
- **Merged Product Lines**: We actively avoided creating intents like "iPhone Issue" or "Mac Issue". Whether a customer is returning an iPhone or a Mac, the agent action (Purchase & Store) is identical. By focusing on *what the customer wants to do* (the verb) rather than *what they own* (the noun), the taxonomy remains compact and useful.
- **Treated "General Complaint" as "Other"**: Twitter datasets contain a massive volume of undirected venting. Rather than forcing these into a technical category, providing an explicit "Complaint/Venting" intent allows the agent to safely respond with empathy and a request for clarification, preventing hallucinations.

## Limitations
- **Temporal Bias**: The dataset was collected around October/November 2017. The intent frequency is massively skewed toward iOS 11 launch bugs. A real-world agent would see a different distribution of these intents year-round, but the taxonomy categories themselves remain fundamentally sound.
- **No Evaluation Yet**: This is a preliminary taxonomy. Its distinctiveness has not yet been proven against an embeddings-based classifier.
