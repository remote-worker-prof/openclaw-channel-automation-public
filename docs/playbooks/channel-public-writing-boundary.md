# Public Writing Boundary Policy (Telegram channels)

## Goal
Keep public channel texts useful and readable for broad audiences.
Do not leak internal operator/agent reasoning into public copy.

## Never publish in public copy
- Internal debugging narration ("I retried API", "SSL error", "tool failed").
- Meta-reasoning about the agent/model process.
- Internal workflow chatter intended for operator logs.
- Over-detailed self-analysis that adds no reader value.
- Private infrastructure details unless they are required for understanding.

## Required transformation rule
If an internal incident must be mentioned publicly:
1. Describe only reader-relevant effect.
2. State concise fix in neutral editorial language.
3. Avoid operator-log tone.
4. Keep trust, avoid drama.
5. Preserve factual scope/time precision ("in this post" vs "in previous releases" must be exact).
6. Prefer generalized lessons (pitfalls/nuances) over chronological incident retelling, unless explicit timeline is requested.
7. If explicit incident detail is requested, use mandatory structure: what happened -> why happened -> how fixed -> where fixed in files/process.

## Style guardrails
- Audience-first perspective.
- Literary technical Russian register.
- Practical clarity over introspective narration.
- No "thinking out loud" paragraphs.
- Explain terms, approaches, and abbreviations in plain language for non-expert readers.
- Replace private/internal project names with generic public terms unless the brand name itself is essential.

## Final pre-publish filter
Before publish, ask:
- "Would this sentence help a reader, or just explain my internal process?"
- "Поймёт ли это читатель без внутреннего контекста команды?"
If not — expand and rewrite.
