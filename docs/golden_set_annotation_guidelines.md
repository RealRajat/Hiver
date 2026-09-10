# Golden Set Annotation Guidelines

## Purpose
The golden evaluation set is a human-labelled ground-truth dataset designed to benchmark the accuracy of the future intent classifier. It provides a reliable standard against which model improvements can be measured.

## Annotation Unit
The unit of annotation is the **First Customer Message** of a reconstructed conversation. 
- The intent classification must primarily rely on the information provided in this initial message.
- Surrounding conversation context (e.g., the brand's reply) may only be used when the first message is highly ambiguous (e.g., "Yes, it is still doing it").

## Decision Rules
- **Deterministic Primary Intent**: When a customer's message contains multiple issues (e.g., "My phone freezes and also I can't login to my Apple ID"), the annotator must select the *primary* intent that dictates the most urgent or relevant support action.
- **Ambiguity Flag**: If a message is genuinely difficult to classify or fits equally well into multiple categories, the `is_ambiguous` flag must be set to `True`, and a brief rationale must be provided in `annotation_notes`.

## Intent Definitions & Boundaries

### 1. Software Bug / Glitch
- **Use when**: The customer reports unexpected software behavior, UI problems, application bugs, or software malfunction in an OS or first-party app.
- **Boundary**: Distinguish from *Device Performance* by focusing on specific functional failures vs. total system failures. "My alarm app didn't ring" = Software Bug. "My phone randomly turns off" = Device Performance.
- **Example**: *"Why did the letter 'I' turn into a question mark after the update?"*

### 2. Device Performance / Hardware
- **Use when**: The primary issue is device-level malfunction, severe performance problems, freezing/crashing, battery drain, or physical hardware problems.
- **Boundary**: Distinguish from *Software Bug* by the severity of the system impact. Freezing, reboot loops, and battery issues are routed here because they typically require hardware diagnostics or replacement.
- **Example**: *"My battery dies in 2 hours since the update."*

### 3. Purchase & Store Operations
- **Use when**: Inquiries relate to purchasing hardware, order status, store pickups, carrier activation, or physical retail experiences.
- **Boundary**: Distinguish from *Services & Account*. Buying an iPhone = Purchase & Store. Buying a movie on iTunes = Services & Account.
- **Example**: *"Can I pick up my pre-ordered iPhone X in store today?"*

### 4. Services & Account
- **Use when**: The issue involves Apple digital services, Apple ID, iCloud, App Store, subscriptions, or digital billing.
- **Boundary**: Includes App Store download issues or Apple Music playing issues, as these are authenticated services rather than local OS bugs.
- **Example**: *"I was billed twice for my Apple Music family plan."*

### 5. How-To / Feature Question
- **Use when**: The customer primarily wants instructions or information about using a feature and is not reporting a malfunction.
- **Boundary**: Look for framing. "How do I turn off the flashlight?" = How-To. "My flashlight won't turn off!" = Software Bug.
- **Example**: *"Does anyone know how to clear the cache on Safari?"*

### 6. General Complaint / Venting (Other)
- **Use when**: The message primarily expresses dissatisfaction or frustration without a specific, actionable support request.
- **Boundary**: If the complaint includes a specific actionable bug ("This update is trash, my camera is black"), route to the specific bug. If it is purely generic ("This update is trash"), route here.
- **Example**: *"Worst update ever, you guys ruined my phone."*

## Human Annotation Workflow
1. The human reviewer opens `data/evaluation/golden_annotation_review_queue.csv`.
2. For each row:
   - Read the `customer_message`.
   - Review the AI-generated `intent` against these guidelines.
   - If incorrect or missing, update it to the exact correct intent string.
   - If ambiguous, ensure `true` is in `ambiguity_flag` and provide reasoning in `annotation_notes`.
   - Once confirmed, update `annotation_source` from `ai_draft` to `human_reviewed`.
3. Save the CSV and commit it as `data/evaluation/golden_set.csv`.

## Limitations
- The current queue is an `ai_draft`. It must NOT be considered ground truth until explicitly reviewed by a human.
