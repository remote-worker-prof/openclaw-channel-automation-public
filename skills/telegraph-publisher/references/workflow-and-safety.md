# Workflow and safety

## Publication policy
- Default mode: draft only.
- Publish only after explicit user confirmation.
- Edit only after explicit user confirmation.
- Do not revoke tokens unless explicitly requested.

## Suggested operator sequence
1. Generate article draft.
2. Discuss and approve article content with Mark.
3. Save draft locally (for audit/history).
4. Run dry-run `telegraph_publish.py`.
5. Show preview + short teaser.
6. On confirmation, run publish mode.
7. Return URL and path.
8. Only then optionally draft/publish Telegram post with article link.

## Instant View strategy
- Use Telegra.ph for dense details, examples, and references.
- Keep channel post short and hook-driven.
- Add one explicit bridge sentence: "Полный разбор: <URL>".

## Failure handling
- If payload > 64KB: split article into parts or trim sections.
- If API error: surface exact error code/text and suggest minimal fix.
- If token missing: stop and request env setup.

## Formatting notes
- Telegraph output must be Node JSON, not Markdown parse_mode.
- Heading support in Telegraph is limited to `h3`/`h4`; map markdown heading tree accordingly.
- Inline markdown markers should be converted before publish to avoid visible artifacts (`**`, `_`, `` ` `` etc.).
