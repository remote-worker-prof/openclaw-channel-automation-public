# Telegram Channel Playbook — algorithmic_planetoid

## Goal
Safe channel management with low blast radius:
1) Draft first
2) Explicit approval before publish
3) No delete/edit by default

See formatting details: `playbooks/telegram-formatting-reference.md`.
See public writing boundary: `playbooks/channel-public-writing-boundary.md`.

## Safety policy
- Allowed by default: `sendMessage`, `sendPhoto`, `sendDocument`, `sendVideo` (new posts only)
- Blocked by default: `deleteMessage`, `editMessage*`, `setWebhook`, `deleteWebhook`
- Any destructive/retroactive action only after explicit one-time confirmation from Mark in chat.

## Connection prerequisites
1. `MATON_API_KEY` is set in environment
2. `TELEGRAM_BOT_TOKEN` is set in environment (preferred route)
3. Bot is admin in channel `@algorithmic_planetoid` with posting rights
4. Telegram connection in Maton can exist, but is not mandatory for publish path

## Verification checklist
- Check API key presence
- Check bot token presence
- `getMe` via `https://gateway.maton.ai/telegram/bot<TOKEN>/getMe` (URL-encoded token)
- `getChat` for `@algorithmic_planetoid`
- Optional smoke test post to a private test chat before channel publish

## Publishing workflow
1. User intent: topic + format + constraints
2. If request includes a long article (`telegra.ph`): discuss/approve article structure and key points first
3. Draft/approve the article
4. Only after article approval: generate 2–3 short post drafts that reference the article
5. User picks/edits one post draft
6. Final preflight (length/markup/link formatting + emoji balance + heading hierarchy for article + public-boundary filter)
7. Publish to channel
8. Save article URL + message ID to memory/daily note

## Content heuristics (for this channel)
- Hook in first 1–2 lines
- 1 core idea per post
- 3–6 concise bullets instead of wall of text
- End with CTA/question
- Optional: one practical snippet/checklist
- When discussing mistakes, frame as generalized pitfalls and practical safeguards (not timeline diary).
- For articles aimed at broad audience, expand meanings of terms and avoid fragmentary shorthand sections.
- Replace private internal naming with generic wording understandable to external readers.

## Emoji policy
- Use emoji as amplifiers, not decoration noise
- Target: usually 1–3 emoji per short post (rarely 4 if format justifies)
- Place at semantic stress points: hook, key contrast, CTA
- Prefer high-signal emoji that fit technical context (e.g., 🔥⚠️✅🚀🧠)
- Avoid repeating the same emoji in consecutive lines

## Telegram formatting policy
- Do NOT use Markdown/MarkdownV2 for channel posts in this pipeline (artifact-prone escaping).
- Default format: HTML (`parse_mode=HTML`) for readable rich styling.
- Fallback format: plain text (no `parse_mode`) if message is too complex or risky.
- In HTML mode, keep to Telegram-supported tags and escape unsafe chars (`<`, `>`, `&`, `"`).

## Fast commands (chat-level convention)
- `черновик поста: <тема>` → generate drafts only
- `опубликуй вариант 2` → publish selected draft
- `сделай серию 5 постов` → content plan, no publish until approval

## Incident policy
If API returns errors / permissions denied:
- Do not retry destructive methods
- Return exact error and next minimal fix step
- Keep user-facing action idempotent where possible

## Archive policy (KnowledgeVault)
- Store each publication in:
  - `/home/sorcerer/KnowledgeVault/04_Проекты/OpenClaw/Каналы/algorithmic_planetoid/<ISO-date>-<post-title-slug>/`
- Keep at least:
  - `article.md`
  - `post.html` (or `post.txt`)
  - `post-meta.md` (URLs, message_id, status)

## Duplicate prevention (mandatory)
- Before publishing a new post, check the publication folder `post-meta.md` for the same `article_url` on the same day.
- If a post for that article already exists, do NOT publish a second similar post unless Mark explicitly asks for an update/repost.
- If repost/update is requested, prefer editing the existing post; if editing is unavailable, publish one replacement and delete the older duplicate.
