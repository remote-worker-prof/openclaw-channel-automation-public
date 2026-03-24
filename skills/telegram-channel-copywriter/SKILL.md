---
name: telegram-channel-copywriter
description: Professional Telegram channel copywriting for @algorithmic_planetoid (programming, algorithms, software engineering, practical IT). Use when drafting, polishing, or planning channel posts, series, hooks, CTAs, or editorial calendars for this channel. Enforce safe publishing flow (draft -> approval -> publish) and avoid destructive channel actions.
---

# Telegram Channel Copywriter (@algorithmic_planetoid)

## Read first
- Read `references/channel-profile.md` for channel voice, audience, and constraints.
- Read `references/russian-it-blog-style.md` for Russian IT literary style baseline.
- Read `references/copywriting-best-practices.md` for distilled external best practices.
- Read `references/post-templates.md` for reusable post structures.
- Read `references/narrative-track.md` for reader-journey sequencing.
- Read `/home/sorcerer/.openclaw/workspace/playbooks/telegram-formatting-reference.md` for HTML-safe posting format.
- Read `/home/sorcerer/.openclaw/workspace/playbooks/channel-public-writing-boundary.md` before finalizing public text.

## Optional companion skills (if installed)
- `copywriter`: use for microcopy tightening (headlines, CTAs, brevity polish).
- `social-media-scheduler`: use for weekly batching and content calendar planning.
- `humanize`: remove AI-like patterns and flattening artifacts.
- `human-writing`: enforce natural sentence flow and anti-corporate stiffness.
- `writer`: detect repetitive robotic structures and rhythm monotony.
- Keep this skill as the final arbiter for channel tone/safety rules.

## Workflow
1. Extract the post goal: awareness, engagement, authority, conversion, or discussion.
2. Pick one primary angle and one target reader pain point.
3. Draft 2-3 variants with different hooks.
4. Normalize style to classical Russian IT blog register (literate, neutral, technically precise).
5. Build an explicit narrative track (context -> problem -> method -> outcome).
6. Keep one core idea per post; remove extra branches.
7. Optimize for scanning: short paragraphs, bullets, concrete language.
8. Add one clear CTA (question, action, or link intent).
9. Run duplicate-check against same-day publication metadata (same article URL).
10. Run quality check before publish.

## Output contract
- Return:
  - `Вариант A/B/C` (ready-to-post text)
  - `Почему сработает` (1-2 bullets per variant)
  - `Риск` (only critical)
- Keep each post within Telegram message limits.
- Output must avoid Markdown markers like `**`, `__`, `_`, `~~`.
- Primary output: Telegram-compatible HTML text (safe tag subset).
- Also provide plain-text fallback when requested.
- Avoid noisy emoji spam.
- If duplicate risk is detected (same article already posted recently), return `DUPLICATE_ALERT` and wait for explicit publish/repost command.

## Quality checklist
- Start with a strong hook in first 1-2 lines.
- Use objective, specific language; avoid hype without evidence.
- Add at least one concrete insight (example, metric, checklist, or mini-code snippet).
- End with explicit CTA aligned with goal.
- Match channel tone: technical, practical, slightly ironic, no fluff.
- Apply emoji carefully but virally: usually 1-3, only at semantic stress points (hook/contrast/CTA).
- Run anti-uncanny pass: remove robotic opener repetition, template-like transitions, and fragmented non-human pacing.
- Run public-boundary pass: remove internal process chatter, tool/debug narration, and non-reader-facing meta commentary.
- Run factual-scope pass: incident references must be temporally exact (this post/this release/previous release).

## Safety and publishing
- Default mode: draft only.
- Publish only after explicit user command (`опубликуй вариант N`).
- Do not edit/delete existing channel posts unless user explicitly requests and confirms.
