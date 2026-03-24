# Russian IT blog style baseline (for @algorithmic_planetoid)

## What to emulate
Based on sampled Russian IT publications (Habr, Selectel, VK technical blog, guide-writing best-practice article):

1. Neutral, literate, non-chatty narration.
2. Clear problem framing -> method -> result.
3. Structured sections with explicit headings.
4. Concrete technical detail (commands, steps, constraints), not abstract motivation.
5. Balanced confidence: no clickbait, no exaggerated claims.
6. Reader-oriented explanation of assumptions and edge cases.

## Language profile
- Literary Russian, modern technical register.
- Precise terminology; no slang unless term is standard in IT.
- Short to medium sentences; avoid overcompression and meme-like rhythm.
- Use "вы" form in instructional segments.
- Remove self-referential personality markers from final copy.

## Composition profile
- Intro: why the topic matters now.
- Main body: 3-7 ordered blocks.
- Each block answers one practical question.
- End: concise conclusion + clear CTA.
- For long-form articles, enforce heading tree: one H1 -> H2 sections -> optional H3 subsections.

## Emoji rule for this channel
- Emoji are allowed but sparse and meaningful.
- Usually 1-3 per short post, aligned with semantic stress points.
- Never replace technical argument with emoji.

## Telegram markup transport rule
- Draft post text semantically first, then render to Telegram-safe HTML.
- Avoid Markdown markers in final text for this pipeline.
- Use Telegram HTML mode by default with supported tags and proper escaping.
- Keep a plain-text fallback variant for fail-safe publishing.

## Source examples (via Exa)
- Habr (Rsync guide): https://habr.com/ru/articles/947630/
- Selectel (IaC/DevOps case): https://selectel.ru/blog/iac-and-devops/
- VK/Habr (Terraform guide): https://habr.com/ru/companies/vk/articles/763282/
- Habr (guide-writing rules): https://habr.com/ru/companies/netologyru/articles/873674
