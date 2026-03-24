# Telegra.ph Python Automation — Current State and Next Steps

## What is already automated (current workspace)

### Existing local stack
- `skills/telegraph-publisher/scripts/telegraph_create_account.py`
- `skills/telegraph-publisher/scripts/telegraph_publish.py` (dry-run by default)
- `skills/telegraph-publisher/scripts/telegraph_edit.py`
- `skills/telegraph-publisher/scripts/telegraph_views.py`
- `skills/telegraph-publisher/scripts/telegraph_common.py`:
  - markdown -> Telegraph Node JSON conversion
  - inline style conversion (`**bold**`, `*italic*`, `` `code` ``, `~~strike~~`, links)
  - ordered/unordered lists and blockquotes
  - heading mapping compatible with Telegraph tag set

### Process already in place
- Article-first workflow for "post + article" requests.
- Dry-run preflight before publish.
- Manual approval gate before create/edit publish action.

## What can be additionally automated (Python)

### Priority A (high ROI)
1. **HTML/Node linter before publish**
   - validate unsupported tags/attrs early
   - detect broken heading tree and malformed links
2. **Payload-aware article splitter**
   - auto-split article when content nears 64KB limit
   - generate part navigation links (Part 1/2/3)
3. **Asset pipeline for images**
   - preprocess local images (resize/compress)
   - upload and replace image URLs in content automatically
4. **Publish bundle transaction**
   - create article -> generate teaser -> post to channel
   - one command with explicit final confirmation

### Priority B (quality + observability)
5. **Versioned snapshots in KnowledgeVault**
   - save source markdown + generated Node JSON + published URL
   - enable audit and roll-forward edits
6. **Link checker**
   - preflight HTTP status checks for all outbound links
7. **Analytics collector**
   - scheduled `getViews` pulls
   - weekly deltas and simple performance dashboard markdown report
8. **Style QA module**
   - validate literary Russian style constraints
   - detect slang/hype patterns and emoji overuse in teaser text

### Priority C (advanced)
9. **A/B teaser generator**
   - produce several Telegram teaser variants for one article
   - compare engagement ex post using view/comment metrics
10. **Editorial calendar integration**
   - queue article drafts and publish windows
   - auto-generate reminder/checklist tasks

## External Python ecosystem (researched)

### Mature wrappers
- `telegraph` (python273) — stable, sync/async support
- `aiograph` — async wrapper
- `telegraph_api` — async wrapper, HTML2Nodes support

### Convenience wrappers
- `html-telegraph-poster-v2`
- `your-telegraph` / YTelegraph (markdown-oriented helper)

## Recommendation for this workspace
- Keep the current local deterministic scripts as the control plane.
- Borrow targeted ideas from external wrappers (e.g., HTML2Nodes helpers, uploader patterns) instead of replacing core flow.
- Implement Priority A first: linter, splitter, asset pipeline, publish bundle.

## Sources (via Exa)
- Official API: https://telegra.ph/api
- python273/telegraph: https://github.com/python273/telegraph
- aiograph: https://github.com/aiogram/aiograph
- telegraph_api: https://github.com/IvanProgramming/Telegraph_api
- html-telegraph-poster-v2: https://pypi.org/project/html-telegraph-poster-v2/
- your-telegraph (YTelegraph): https://github.com/alterxyz/YTelegraph
