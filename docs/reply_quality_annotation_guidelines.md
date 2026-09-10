# Reply Quality Annotation Guidelines

## Purpose
This document provides a clear rubric for human judges evaluating drafted support replies. These scores will establish a baseline to measure the quality of automated support responses and to benchmark LLM-as-judge agreement.

## Evaluation Dimensions
Every generated reply must be evaluated on a 1–5 scale across five specific dimensions, plus an Overall Score.

### 1. Helpfulness
How useful is the reply in actually resolving the customer's issue?
- **1 (Unacceptable)**: Completely unhelpful, dismissive, or actively harmful.
- **2 (Poor)**: Barely helpful; points in a vague direction but lacks actionable steps.
- **3 (Acceptable)**: Resolves part of the issue or provides a generic but accurate resource.
- **4 (Good)**: Addresses the issue directly with clear next steps.
- **5 (Excellent)**: Completely resolves the issue with exceptional clarity and anticipating follow-up needs.

### 2. Correctness
Does the response accurately address the customer's actual issue without making factually wrong statements? (Do not confuse "sounds good" with "correct".)
- **1 (Unacceptable)**: Blatantly incorrect or solves the wrong problem entirely.
- **2 (Poor)**: Contains major factual errors or mostly misses the point.
- **3 (Acceptable)**: Technically correct but misses important nuances of the specific issue.
- **4 (Good)**: Correctly diagnoses and addresses the issue with minor omissions.
- **5 (Excellent)**: Perfectly correct, precise, and directly addresses the core issue.

### 3. Relevance
Is the information provided strictly relevant to the specific customer inquiry?
- **1 (Unacceptable)**: Totally irrelevant to the customer's message.
- **2 (Poor)**: Contains mostly boilerplate or irrelevant information with a tiny relevant piece.
- **3 (Acceptable)**: Relevant, but includes unnecessary filler or tangential information.
- **4 (Good)**: Highly relevant with very minimal fluff.
- **5 (Excellent)**: Directly and concisely relevant to exactly what was asked.

### 4. Groundedness
Does the reply stay supported *strictly* by the provided historical evidence?
- **1 (Unacceptable)**: Pure hallucination; invents policies, URLs, or promises refunds not present in evidence.
- **2 (Poor)**: Heavily relies on unprovided outside knowledge; hallucinates troubleshooting steps.
- **3 (Acceptable)**: Mostly grounded, but makes minor assumptions not strictly in the text.
- **4 (Good)**: Strongly grounded in the provided historical evidence.
- **5 (Excellent)**: Perfectly grounded; makes zero unsupported claims or fabrications.

### 5. Tone
Is the tone professional, empathetic, and aligned with AppleSupport standards?
- **1 (Unacceptable)**: Rude, condescending, or extremely robotic/impersonal.
- **2 (Poor)**: Curt, cold, or slightly inappropriate for customer service.
- **3 (Acceptable)**: Neutral and polite, but generic.
- **4 (Good)**: Professional, friendly, and empathetic.
- **5 (Excellent)**: Warm, highly empathetic, and perfectly captures the ideal support persona.

### 6. Overall Score
A holistic judgment of the reply's quality as a final support asset.
- **1 (Unacceptable)**: Cannot be sent. Requires total rewrite or human escalation.
- **2 (Poor)**: Requires heavy editing before it could be sent.
- **3 (Acceptable)**: Could be sent in a pinch, but could easily be better.
- **4 (Good)**: Ready to send with minor or no tweaks.
- **5 (Excellent)**: A perfect support interaction.

## Important Rules
- **Do not assume hidden context**: Only judge based on the provided customer message and historical evidence.
- **Penalize hallucinations**: A response that sounds great but invents a fake "apple.com/fake-fix" link must receive a `1` in Groundedness.
- **Separate Tone from Correctness**: A beautifully polite answer that gives wrong instructions should score a `5` in Tone but a `1` or `2` in Correctness.
- **Notes**: Use the `judge_notes` column to briefly explain any score of 1, 2, or 5 to help refine future LLM models.
