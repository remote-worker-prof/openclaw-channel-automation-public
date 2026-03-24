# Long-form article structures (Telegra.ph)

## Heading hierarchy policy (mandatory)
- Start article with exactly one H1 (`# ...`) as the title.
- Use H2 (`## ...`) for main sections.
- Use H3 (`### ...`) only for subsections inside an H2.
- Do not skip levels (H1 -> H3 without H2 is forbidden).
- Keep heading tree consistent in the entire article.

## Narrative policy (mandatory)
- Lead the reader through explicit sequence: context -> problem -> method -> implementation -> checks -> conclusion.
- Add transition lines between sections so the article reads as a continuous route, not isolated blocks.

## Template A — Deep technical explainer
1. Hook: what problem hurts in practice
2. Why common approach fails
3. Correct mental model
4. Step-by-step implementation
5. Edge cases and anti-patterns
6. Checklist / takeaway

## Template B — Case study
1. Context and constraints
2. Options considered
3. Decision and rationale
4. Execution details
5. Result + metrics
6. Lessons learned

## Template C — Practical guide
1. Goal and prerequisites
2. Core concepts (compact)
3. Procedure (ordered steps)
4. Example
5. Troubleshooting
6. FAQ

## Bridge snippet for channel post
- "Коротко: <insight>."
- "Полный разбор с деталями и примерами: <telegra.ph URL>."
