---
name: telegraph-publisher
description: Create and update long-form Telegra.ph articles for Telegram content expansion. Use when the user wants a detailed companion article, Instant View-friendly deep dive, or a long-form appendix linked from a short channel post. Supports safe flow: draft -> approval -> publish -> optional link in Telegram post.
---

# Telegraph Publisher

## Read first
- Read `references/telegraph-api-quickref.md` for API limits/methods.
- Read `references/workflow-and-safety.md` for publication policy.
- Read `references/article-structure.md` for long-form layout templates.
- Read `/home/sorcerer/.openclaw/workspace/plans/telegraph-python-automation-roadmap.md` for current automation scope and extension plan.
- Read `/home/sorcerer/.openclaw/workspace/playbooks/channel-public-writing-boundary.md` for public editorial limits.
- Use classical Russian IT blog style (neutral, literate, technically precise).

## Core flow
1. Define article objective and target reader.
2. Draft article in markdown/text.
3. Run anti-uncanny rewrite pass (human rhythm, smoother transitions, no template stiffness).
4. Run dry-run preview via `scripts/telegraph_publish.py` (default mode).
5. Ask for explicit approval before `--publish`.
6. Return URL + short teaser line for Telegram post.
7. Link article in channel post only on explicit user command.

## Commands
- Create account (one-time): `scripts/telegraph_create_account.py`
- Create page: `scripts/telegraph_publish.py`
- Edit page: `scripts/telegraph_edit.py`
- Views: `scripts/telegraph_views.py`

## Defaults
- Never publish without explicit confirmation.
- Never silently edit existing published pages.
- Prefer concise Telegram post + Telegra.ph deep article pairing.
- Ensure content is converted to valid Telegraph Node JSON (no raw Markdown artifacts in published text).
- Remove internal operator/model/tooling narration from public article text unless strictly reader-relevant.
- Keep incident wording temporally exact (avoid vague backdating like "one of previous releases" when issue was in current post).

## Output contract
Return:
- `Черновик` (article text)
- `Telegra.ph preview` (title, est. payload size, publish mode)
- `Готовая ссылка` (after approval + publish)
- `Текст-тизер` for channel (1-3 lines)

Formatting requirements:
- enforce heading hierarchy starting from H1 (`#`), then H2 (`##`), then H3 (`###`);
- no heading-level jumps.
