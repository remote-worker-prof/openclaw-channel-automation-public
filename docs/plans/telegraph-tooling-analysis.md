# Telegra.ph tooling analysis for OpenClaw

## Goal
Create long-form Telegra.ph articles from chat, then (optionally) attach article links in Telegram channel posts.

## Current baseline
- Telegram posting is already operational via Maton gateway for `@algorithmic_planetoid`.
- No dedicated Telegra.ph MCP server is currently configured.

## Minimal viable stack (recommended)

### 1) New local skill: `telegraph-publisher`
Purpose: deterministic article creation workflow with safety checks.

Include:
- `SKILL.md` (trigger + workflow)
- `scripts/telegraph_create.py`
- `scripts/telegraph_edit.py`
- `scripts/telegraph_get_views.py`
- `references/telegraph-content-rules.md`

### 2) Secrets/config
- `TELEGRAPH_ACCESS_TOKEN` (env)
- Optional defaults:
  - `TELEGRAPH_AUTHOR_NAME`
  - `TELEGRAPH_AUTHOR_URL`

### 3) API methods to support first
- `createAccount` (one-time bootstrap)
- `createPage`
- `editPage`
- `getPage`
- `getViews`
- Optional: `getPageList`

### 4) Content pipeline
1. Draft article in Markdown-like internal format.
2. Convert to Telegraph Node JSON (`p`, `h3`, `h4`, `ul`, `ol`, `li`, `blockquote`, `pre`, `code`, `a`, `img`).
3. Validate limits (content payload, title length, allowed tags/attrs).
4. Create page on Telegra.ph.
5. Return URL + short summary for Telegram post.
6. Publish link to channel only after explicit approval.

## Optional MCP layer (only if you want strict tool isolation)

### Option A (pragmatic): no extra MCP server
- Use local scripts from skill + existing OpenClaw tools.
- Fastest and sufficient for reliable publishing.

### Option B (advanced): custom MCP `telegraph-mcp`
- Wrap Telegra.ph API endpoints as MCP tools:
  - `telegraph.create_page`
  - `telegraph.edit_page`
  - `telegraph.get_page`
  - `telegraph.get_views`
- Pros: typed tools, cleaner orchestration, safer interface boundaries.
- Cons: higher setup and maintenance overhead.

## Safety model (must-have)
- Default: draft only.
- Require explicit command for publish/link-in-channel.
- No silent edits of existing Telegra.ph pages.
- Keep immutable local snapshot of each published article (markdown + API payload + URL).

## Integration with channel copywriter skill
- Short channel post remains in `telegram-channel-copywriter` flow.
- If detail depth required: append CTA link to Telegra.ph article.
- Pattern:
  - `короткий пост` (hook + key insight + CTA)
  - `длинный разбор` on Telegra.ph

## Why this is enough
- Telegra.ph API is simple HTTPS JSON, no heavy SDK/MCP dependency required.
- Main complexity is content conversion + approval safety, best handled by a focused local skill.
