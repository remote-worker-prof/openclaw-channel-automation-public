# Telegra.ph API quick reference

Base URL:
- `https://api.telegra.ph/<method>`

Core methods for this skill:
- `createAccount`
- `createPage`
- `editPage`
- `getPage`
- `getPageList`
- `getViews`
- `revokeAccessToken`

Key limits:
- `title`: 1-256 chars
- `author_name`: 0-128 chars
- `author_url`: 0-512 chars
- `content`: array of Nodes, up to 64KB payload

Supported content tags (important subset):
- `p`, `h3`, `h4`, `blockquote`, `pre`, `code`, `ul`, `ol`, `li`, `a`, `img`, `figure`, `figcaption`, etc.

Response format:
- Always JSON with `ok: true/false`
- Success payload in `result`
- Error text in `error`

Security note:
- Keep `TELEGRAPH_ACCESS_TOKEN` in env, not inside prompts.

Anti-artifact rules:
- Telegraph does not accept Markdown as a parse mode parameter.
- API expects `content` as JSON array of Nodes (`NodeElement`/text nodes).
- Keep heading logic compatible with Telegraph tags (`h3`/`h4` in payload).
- Prefer deterministic conversion (markdown -> node JSON) over raw HTML paste.

Source:
- https://telegra.ph/api
