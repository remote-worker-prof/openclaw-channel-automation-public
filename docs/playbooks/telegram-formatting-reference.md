# Telegram formatting reference (channel pipeline)

## Policy summary
- Markdown/MarkdownV2: disabled for publishing in this pipeline.
- Preferred: `parse_mode=HTML` with strict safe subset.
- Fallback: plain text (`parse_mode` omitted).

## HTML subset to use
- Bold: `<b>...</b>` / `<strong>...</strong>`
- Italic: `<i>...</i>` / `<em>...</em>`
- Underline: `<u>...</u>`
- Strike: `<s>...</s>`
- Spoiler: `<tg-spoiler>...</tg-spoiler>`
- Link: `<a href="https://...">...</a>`
- Inline code: `<code>...</code>`
- Block code: `<pre><code class="language-python">...</code></pre>`
- Blockquote: `<blockquote>...</blockquote>`

## Escaping rules
In HTML mode, escape text outside tags:
- `&` -> `&amp;`
- `<` -> `&lt;`
- `>` -> `&gt;`
- `"` -> `&quot;` (when needed)

## Practical guidance for channel posts
- Keep paragraphs short and skimmable.
- Use formatting to guide reading, not to decorate every line.
- Emoji: 1-3 per post, aligned to hook/contrast/CTA.

## Sources
- Telegram Bot API formatting options: https://core.telegram.org/bots/api#formatting-options
- Telegram Bot API HTML style: https://core.telegram.org/bots/api#html-style
