# Agent Pipeline Evaluation Report

**Evaluation Size**: 200 examples

## Intent Metrics
- **Accuracy**: 0.3450
- **Macro F1**: 0.0855

## Retrieval Metrics
- **Coverage**: 100.0%
- **Proxy Intent Hit Rate**: 34.5%

## Pipeline Metrics
- **Auto-Handle Rate**: 100.0% (200)
- **Escalation Rate**: 0.0% (0)

## Representative Examples

### Successfully Auto-Handled

**ID**: GOLDEN_001
- **Message**: @AppleSupport how long until you fix the keyboard issues with the autocorrecting of letters?
- **Intent**: Software Bug / Glitch
- **Draft**: This is a mocked safe LLM response based on the evidence.

**ID**: GOLDEN_002
- **Message**: @AppleSupport you seem to be skipping the step that allows to select which carrier phone to get for iPhone X upgrade head start. Why?
- **Intent**: Software Bug / Glitch
- **Draft**: This is a mocked safe LLM response based on the evidence.

**ID**: GOLDEN_003
- **Message**: Bruhhhh I’m so fuckin tired @AppleSupport @115858 fixed these damn glitches ! Keep cutting my phone off
- **Intent**: Software Bug / Glitch
- **Draft**: This is a mocked safe LLM response based on the evidence.

**ID**: GOLDEN_004
- **Message**: What is this “A” and  QUESTION MARK THAT MY PHONE KEEPS DOING!! @115858 @AppleSupport
- **Intent**: Software Bug / Glitch
- **Draft**: This is a mocked safe LLM response based on the evidence.

**ID**: GOLDEN_005
- **Message**: @AppleSupport any way to actually talk to a store? I've tried 0117 959 7600 (Bristol) and just end up back with AppleCare or Sales each time
- **Intent**: Software Bug / Glitch
- **Draft**: This is a mocked safe LLM response based on the evidence.

### Escalated to Human

## Limitations
- The draft replies are purely deterministic extractions and are not evaluated for stylistic or contextual accuracy.
- The retrieval proxy hit rate evaluates the top-1 result only.
- No fabricated human/LLM agreement scores are included, as they are not yet supported by an active LLM.
