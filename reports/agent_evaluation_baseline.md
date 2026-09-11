# Agent Pipeline Evaluation Report

**Evaluation Size**: 200 examples

## Intent Metrics
- **Accuracy**: 0.4750
- **Macro F1**: 0.4214

## Retrieval Metrics
- **Coverage**: 100.0%
- **Top-1 Proxy Intent Hit Rate**: 36.0%

## Pipeline Metrics
- **Auto-Handle Rate**: 51.0% (102)
- **Escalation Rate**: 49.0% (98)

## Representative Examples

### Successfully Auto-Handled

**ID**: GOLDEN_001
- **Message**: @AppleSupport how long until you fix the keyboard issues with the autocorrecting of letters?
- **Intent**: Software Bug / Glitch
- **Draft**: Based on historical cases with similar Software Bug / Glitch issues, Apple Support typically advises:

"@454673 We'd like to hear more about what's going on. Please DM us about this issue and we'll continue there. https://t.co/GDrqU22YpT"

**ID**: GOLDEN_009
- **Message**: Aye @115858 y’all are gonna need to send another update. Every time I️ type an “I️” it ends up looking like this 😒 https\://t.co/zqG2JxPR3V
- **Intent**: Software Bug / Glitch
- **Draft**: Based on historical cases with similar Software Bug / Glitch issues, Apple Support typically advises:

"@240819 We'd love to look into this concern with you further. Meet us in DM to continue please: https://t.co/GDrqU2kzhr"

**ID**: GOLDEN_010
- **Message**: @AppleSupport with iOS11 my phone won’t show my music on my lock screen and when I receive calls I can’t hear anything on the other end help
- **Intent**: Device Performance / Hardware
- **Draft**: Based on historical cases with similar Device Performance / Hardware issues, Apple Support typically advises:

"@753808 Thanks for reaching out. Let us know if this helps: https://t.co/XlmCP2gCtj"

**ID**: GOLDEN_011
- **Message**: @AppleSupport  I updated to iOS 11.0.3 on my 6s plus &amp; I just went from 85% to 13% in an hour after watching two YouTube videos. :/
- **Intent**: Software Bug / Glitch
- **Draft**: Based on historical cases with similar Software Bug / Glitch issues, Apple Support typically advises:

"@590744 Hey there! We'd be happy to look into this with you, but we'll need some background first. Shoot us a DM and we'll go from there. https://t.co/GDrqU22YpT"

**ID**: GOLDEN_012
- **Message**: @AppleSupport Since updating to iOS 11 I’m not receiving text alerts on my watch now yet I receive them for WhatsApp &amp; calls 😤
- **Intent**: Software Bug / Glitch
- **Draft**: Based on historical cases with similar Software Bug / Glitch issues, Apple Support typically advises:

"@335480 We want to help.  If you go to Settings &gt; Notifications &gt; WhatsApp, are notifications turned on?"

### Escalated to Human

**ID**: GOLDEN_002
- **Message**: @AppleSupport you seem to be skipping the step that allows to select which carrier phone to get for iPhone X upgrade head start. Why?
- **Intent**: General Complaint / Venting (Other)
- **Reason**: General complaints and venting require empathetic human handling or are non-actionable.

**ID**: GOLDEN_003
- **Message**: Bruhhhh I’m so fuckin tired @AppleSupport @115858 fixed these damn glitches ! Keep cutting my phone off
- **Intent**: General Complaint / Venting (Other)
- **Reason**: General complaints and venting require empathetic human handling or are non-actionable.

**ID**: GOLDEN_004
- **Message**: What is this “A” and  QUESTION MARK THAT MY PHONE KEEPS DOING!! @115858 @AppleSupport
- **Intent**: General Complaint / Venting (Other)
- **Reason**: General complaints and venting require empathetic human handling or are non-actionable.

**ID**: GOLDEN_005
- **Message**: @AppleSupport any way to actually talk to a store? I've tried 0117 959 7600 (Bristol) and just end up back with AppleCare or Sales each time
- **Intent**: Purchase & Store Operations
- **Reason**: Purchase & Store Operations issues frequently require secure account verification or transaction management.

**ID**: GOLDEN_006
- **Message**: WHY IS THE LETTER I SHOWING UP AS A QUESTION MARK IN A BOX ? @115858 FIX IT
- **Intent**: General Complaint / Venting (Other)
- **Reason**: General complaints and venting require empathetic human handling or are non-actionable.

## Limitations
- The draft replies are purely deterministic extractions and are not evaluated for stylistic or contextual accuracy.
- The retrieval proxy hit rate evaluates the top-1 result only.
- No fabricated human/LLM agreement scores are included, as they are not yet supported by an active LLM.
